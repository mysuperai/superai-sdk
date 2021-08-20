from typing import Optional


class SuperTracker:
    def __init__(self, path: Optional[str] = None):
        super().__init__()
        self.path = path

    def add_scalar(self, tag, scalar_value, global_step=None, walltime=None):
        pass

    def add_scalars(self, main_tag, tag_scalar_dict, global_step=None, walltime=None):
        pass

    def add_histogram(self, tag, values, global_step=None, bins="tensorflow", walltime=None, max_bins=None):
        pass

    def add_image(self, tag, img_tensor, global_step=None, walltime=None, dataformats="CHW"):
        pass

    def add_images(self, tag, img_tensor, global_step=None, walltime=None, dataformats="NCHW"):
        pass

    def add_figure(self, tag, figure, global_step=None, close=True, walltime=None):
        pass

    def add_video(self, tag, vid_tensor, global_step=None, fps=4, walltime=None):
        pass

    def add_audio(self, tag, snd_tensor, global_step=None, sample_rate=44100, walltime=None):
        pass

    def add_text(self, tag, text_string, global_step=None, walltime=None):
        pass

    def add_embedding(self, mat, metadata=None, label_img=None, global_step=None, tag="default", metadata_header=None):
        pass

    def add_pr_curve(self, tag, labels, predictions, global_step=None, num_thresholds=127, weights=None, walltime=None):
        pass

    def add_mesh(self, tag, vertices, colors=None, faces=None, config_dict=None, global_step=None, walltime=None):
        pass

    def add_hparams(self, hparam_dict, metric_dict, hparam_domain_discrete=None, run_name=None):
        pass
