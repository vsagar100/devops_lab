# devops_lab

## Senario1: 
    There is backend service app called `checkout-api` build on top of python and fast-api. Uptime is most important for this app. Devloper will mae change in `dev` branch. 
Once developer complete the code and unit testing on his machine he will raise the PR. Upon PR dev -> main, CI pipeline workflow should trigger.
    - It should do some sanity testing, 
    - Build the docker image
    - Push image to ACR
Upon push to `main` branch, the CD workflow should trigger
    - It should pull the latest image from ACR
    - Perform the testing
    - Update image in Kubernetes cluster
    - Check the status of app
    - If unsuccessful then rollback changes
    - Upload the artifacts
