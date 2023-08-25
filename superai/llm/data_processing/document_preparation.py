import logging
from typing import Dict, List, Optional

import tiktoken


class DocumentToString:
    def __init__(
        self,
        format_kv_checkboxes: bool,
        format_tables: bool,
        representation: str,
        max_pages: Optional[int],
        max_token: int,
        pixels_per_line: int = 10,
        pixels_per_char: int = 4,
        tokenizer_model: str = "gpt-3.5-turbo",
        include_line_number: bool = False,
    ):
        """Creates an instance of a document to string converter.

        This class helps to convert OCR outputs of documents into a string that is more suitable for usage within LLM
        prompting. Currently, two different representation methods are implemented. Line based representation keeps some
        spatial information of the input document while remaining fairly compact. The whitespace representation will
        give a higher degree of spatial consistency.


        :param format_kv_checkboxes: Will include standardized checkbox output into target string
        :param format_tables: Currently not implemented. Plan: Include standardized table format into target string
        :param representation: Output representation: `whitespace` or `line`
        :param max_pages: Number of pages that will be converted
        :param max_token: Limit of tokens each output chunk will maximally have once encoded for LLM
        :param pixels_per_line: Assumed average height of a character only relevant for whitespace representation
        :param pixels_per_char: Assumed average width of a character only relevant for whitespace representation
        :param include_line_number: Will add a line number at the beginning of each line in the output representation
        :param tokenizer_model:
        """
        self.format_kv_checkboxes = format_kv_checkboxes
        self.format_tables = format_tables
        self.representation = representation
        self.max_pages = max_pages
        self.max_token = max_token
        self.pixels_per_line = pixels_per_line
        self.pixels_per_char = pixels_per_char
        self.tokenizer_model = tokenizer_model
        self.include_line_number = include_line_number

    def get_document_representation(
        self, ocr_values: list, ocr_key_values: Optional[list], ocr_general_tables: Optional[list]
    ) -> List[str]:
        """Takes the unified OCR output and turns it into a serialized string that preserves spatial information of the
        original document. This string is separated into chunks such that each of the chunks will be of `max_size` once
        encoded for LLM.

        The function will take the OCR token and depending on the representation style use the bounding boxes to insert
        additional tokens into the target string. The target string is limited to `max_pages` and will be split into
        parts such that the size of each chunk does not exceed `max_token` once encoded for LLM. Each chunk will only
        include complete documents.

        If `format_kv_checkboxes` is set, the function will replace OCR tokens at those locations with a standardized
        format. It will choose key-[ ] for unchecked checkboxes and key-[X] for checked checkboxes.

        :param ocr_values: List of OCR tokens
        :param ocr_key_values:  List of key value pairs
        :param ocr_general_tables: List of OCR tables
        :return:
        """
        doc_iterator = self._get_per_page_representation(ocr_values, ocr_key_values, ocr_general_tables)
        doc_iterator = doc_iterator[: self.max_pages]
        return self._get_string_chunks(doc_iterator, page_separation=False)

    def _get_per_page_representation(self, ocr_values, ocr_key_values, ocr_general_tables):
        if self.format_kv_checkboxes:
            if ocr_key_values is not None:
                ocr_values = _replace_checkbox_kv_pairs(ocr_values, ocr_key_values)
            else:
                logging.info("No key value pairs were provided to be included into document serialization")
        if self.format_tables:
            raise NotImplementedError("Table inclusion is not implemented")

        # Combine tokens into String representation
        if self.representation == "line":
            return get_line_based_representation(ocr_values)
        elif self.representation == "whitespace":
            return get_white_space_representation(
                ocr_values, pixels_per_line=self.pixels_per_line, pixels_per_char=self.pixels_per_char
            )
        else:
            raise NotImplementedError(f"There is no document representation of type {self.representation}")

    def _get_string_chunks(self, per_page_representation, page_separation=False):
        """Splitting mechanism that will fill up chunks line by line until max token length is reached. If
        page_separation is set a new chunk will be created for every page.

        :param per_page_representation: List of string containing the text representation of the input document
        :param page_separation: Will force splitter to create a new chunk once a new page is processed
        :return: List of chunks with max token length in encoding space
        """
        encoder = tiktoken.encoding_for_model(self.tokenizer_model)

        included_lines = []
        document_chunks = []
        chunk_length = 0
        line_number = 0
        for page in per_page_representation:
            lines = page.split("\n")
            for line in lines:
                line_number_seq = f"{line_number}:  " if self.include_line_number else ""
                final_line = line_number_seq + line
                updated_chunk_length = len(encoder.encode("\n".join(included_lines + [final_line])))
                if updated_chunk_length > self.max_token and not included_lines:
                    raise ValueError(
                        f"Line has {updated_chunk_length} token. This is more than the {self.max_token} per chunk. "
                        f"Please increase chunk size of input representation."
                    )

                if updated_chunk_length < self.max_token:
                    chunk_length += updated_chunk_length
                    included_lines.append(final_line)
                else:
                    document_chunks.append("\n".join(included_lines))
                    included_lines = [final_line]
                    chunk_length = len(encoder.encode(final_line))

                line_number += 1

            if page_separation:
                document_chunks.append("\n".join(included_lines))
                included_lines = []
                chunk_length = 0

        document_chunks.append("\n".join(included_lines))

        # Avoid returning empty chunks
        filtered_document_chunks = [chunk for chunk in document_chunks if len(chunk) > 0]

        return filtered_document_chunks

    def get_white_space_line_dict(self, ocr_values: List[dict]) -> Dict[int, list]:
        """Collects ocr tokens by the line they are assigned to in the white space representation.

        :param ocr_values: List of ocr values in standard format
        :return: A dictionary indexed by the line in white space representation and a list of token
        """
        # Part of this code a duplicated from the actual white space representaiton
        # Sort tokens by page number, y-position in grid and x-position in grid
        ocr_values.sort(
            key=lambda ocr_token: (
                ocr_token["pageNumber"],
                ocr_token["boundingBox"]["top"] // self.pixels_per_line,
                ocr_token["boundingBox"]["left"] // self.pixels_per_char,
            )
        )

        line_base = 0
        line_id = 0
        current_page = 1
        line_dict = {}
        for token in ocr_values:
            page_number = token["pageNumber"]
            # Handle new page
            if page_number > current_page:
                line_base += line_id + 1  # Pages are separated with a new line
                current_page = page_number

            line_id = token["boundingBox"]["top"] // self.pixels_per_line
            line_number = line_base + line_id
            line_dict.setdefault(line_number, []).append(token)
        return line_dict


def _replace_checkbox_kv_pairs(ocr_values, ocr_key_values):
    kv = [item for item in ocr_key_values if "value" in item]
    kv = [item for item in kv if item["value"]["content"] == ":selected:" or item["value"]["content"] == ":unselected:"]
    kv = _deduplicate_boxes(kv)
    for e in kv:
        page_number = e["value"]["pageNumber"]
        checkbox_bbox = e["key"]["boundingBox"]
        value_bbox = e["value"]["boundingBox"]
        box_str = "[ ]" if e["value"]["content"] == ":unselected:" else "[X]"
        content = f"{e['key']['content']}-{box_str}"

        ocr_values = filter_tokens_by_text_box(ocr_values, checkbox_bbox, page_number)
        ocr_values = filter_tokens_by_text_box(ocr_values, value_bbox, page_number)

        ocr_values.append({"content": content, "boundingBox": checkbox_bbox, "pageNumber": page_number})
    return ocr_values


def _deduplicate_boxes(kv_list):
    keep = []
    matched = []
    for i, kv_pair in enumerate(kv_list):
        for j in range(i + 1, len(kv_list)):
            other_kv = kv_list[j]
            if intersect(kv_pair["key"]["boundingBox"], other_kv["key"]["boundingBox"]) and (
                kv_pair["key"]["pageNumber"] == other_kv["key"]["pageNumber"]
            ):
                matched.append(j)
        if i not in matched:
            keep.append(kv_pair)
    return keep


def intersect(box1, box2):
    """
    Tests whether two bounding boxes intersect.
    """
    # Determine the coordinates of the bounding boxes
    box1_top = box1["top"]
    box1_bottom = box1["top"] + box1["height"]
    box1_left = box1["left"]
    box1_right = box1["left"] + box1["width"]

    box2_top = box2["top"]
    box2_bottom = box2["top"] + box2["height"]
    box2_left = box2["left"]
    box2_right = box2["left"] + box2["width"]

    # Check for intersection
    if box1_left < box2_right and box1_right > box2_left and box1_top < box2_bottom and box1_bottom > box2_top:
        return True
    else:
        return False


def filter_tokens_by_text_box(tokens, text_box, page_number):
    kept_tokens = []
    text_area = text_box["width"] * text_box["height"]
    for token in tokens:
        # Extract the bounding box from the token dictionary
        bbox = token["boundingBox"]
        # Calculate the intersection between the token and text boxes
        x1 = max(bbox["left"], text_box["left"])
        y1 = max(bbox["top"], text_box["top"])
        x2 = min(bbox["left"] + bbox["width"], text_box["left"] + text_box["width"])
        y2 = min(bbox["top"] + bbox["height"], text_box["top"] + text_box["height"])
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        # Check if the token area within the text area is at least 90%
        token_area = bbox["width"] * bbox["height"]
        if not (token["pageNumber"] == page_number and token_area <= text_area and intersection >= 0.9 * token_area):
            kept_tokens.append(token)
    return kept_tokens


def get_line_based_representation(ocr_outputs, tolerance=2):
    sorted_ocr = sorted(
        ocr_outputs,
        key=lambda x: (
            x["pageNumber"],
            x["boundingBox"]["top"] + x["boundingBox"]["height"] / 2,
            x["boundingBox"]["left"],
        ),
    )
    pages = []
    current_page = []
    current_line = []
    prev_middle_y = None

    for ocr in sorted_ocr:
        middle_y = ocr["boundingBox"]["top"] + ocr["boundingBox"]["height"] / 2
        if prev_middle_y is not None and abs(middle_y - prev_middle_y) > tolerance:
            line_string = " ".join([t["content"] for t in sorted(current_line, key=lambda x: x["boundingBox"]["left"])])
            current_page.append(line_string)
            current_line = []
        if ocr["pageNumber"] != len(pages) + 1:
            pages.append("\n".join(current_page))
            current_page = []

        current_line.append(ocr)
        prev_middle_y = middle_y

    if current_line:
        line_string = " ".join([t["content"] for t in sorted(current_line, key=lambda x: x["boundingBox"]["left"])])
        current_page.append(line_string)
    if current_page:
        pages.append("\n".join(current_page))
    return pages


def get_white_space_representation(ocr_values, pixels_per_line=10, pixels_per_char=4):
    """This function will obtain a spatially sound text representation of the input document.

    The document is split into a grid of characters. If there is no OCR token, that would fit into the grid, a space or
    new line is inserted into the target string. Additional white spaces are inserted after a token to avoid those token
    to be merged together.

    :param ocr_values: List of OCR tokens in unified format
    :param pixels_per_line: Assumed average height of a character
    :param pixels_per_char: Assumed average width of a character
    :return: String representation of the document
    """
    # Sort tokens by page number, y-position in grid and x-position in grid
    ocr_values.sort(
        key=lambda ocr_token: (
            ocr_token["pageNumber"],
            ocr_token["boundingBox"]["top"] // pixels_per_line,
            ocr_token["boundingBox"]["left"] // pixels_per_char,
        )
    )

    # Initialize the document
    page_tokens = []
    doc_pages = []

    # Variables to track the current position
    current_page = 1
    current_line = 0
    for token in ocr_values:
        # Combine all token for a page together and add them to the result.
        while token["pageNumber"] > current_page:
            doc_pages.append("".join(page_tokens))
            page_tokens = []
            current_page += 1
            current_line = 0

        # Add newlines if necessary
        lines_needed = max(1, token["boundingBox"]["top"] // pixels_per_line)
        while current_line < lines_needed:
            page_tokens.append("\n")
            current_line += 1

        # Add spaces for horizontal position
        char_pos = int(token["boundingBox"]["left"] // pixels_per_char)
        if len(page_tokens[current_line - 1]) < char_pos:
            page_tokens[current_line - 1] += " " * (char_pos - len(page_tokens[current_line - 1]))

        # Add the word token. Also add an extra white space to avoid that tokens will be fused together
        page_tokens[current_line - 1] += token["content"] + " "
    doc_pages.append("".join(page_tokens))

    return doc_pages
