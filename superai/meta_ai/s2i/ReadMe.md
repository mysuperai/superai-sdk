# Source to Image AI encapsulation

To replace pickling, source to image (s2i) is a viable alternative to pass model logic from user. 

For the examples to run, you would need the source-to-image package installed. 

### Installation
From the [reference here](https://github.com/openshift/source-to-image#installation)
####MacOs
You can install on MacOs using
```bash
brew install source-to-image
```
#### Linux
For linux systems, download
```bash
mkdir /tmp/s2i/ && cd /tmp/s2i/ 
curl -s https://api.github.com/repos/openshift/source-to-image/releases/latest \
  | grep browser_download_url \
  | grep linux-amd64 \
  | cut -d '"' -f 4 \
  | wget -qi -
```
Unpack the downloaded tar file
```bash
$ tar xvf source-to-image*.gz
./
./s2i
./sti
```
Move the executable to `/usr/local/bin`
```bash
sudo mv s2i /usr/local/bin
rm -rf /tmp/s2i/
```
## Building Base Image
To create a base image to be utilized for s2i image creation, you would need to build the container and push it on the container registry from the `builder` folder
```bash
cd builder
make build
# build kubernetes container
make build-seldon
```
By default this uses a `x86_64` base image. For `ARM64` based images you can use `make build TARGET_PLATFORM=linux/arm64`. For using Cuda, you can specify `mode=gpu` in the make command above.

Any specific build logic can be changed in the `builder/s2i/bin` folder. 

> Currently, incremental build is an open task. But otherwise the general scripts run well.

## Testing
Testing the above made base image can be done using the contents in the `basic_test` folder. Please note that in the usage of this module, all files in `basic_test` folder will be generated dynamically.

To run the end-to-end test with the container built in the previous step, run the following from the tests
```bash
cd tests/meta_ai/s2i_test
make folder=<test folder> test
```
Verify the Makefile to see what's happening in the background
