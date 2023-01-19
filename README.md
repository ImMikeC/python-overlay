# FastAPI endpoints for handling images stored in Azure Blob Container account.
## Image files.
You can see, download, upload, delete and overlay images files (blobs) stored in an Azure Storage Container.
This can be done with FastAPI, Uvicorn, Pillow (PIL) and Azure Functions.

## How to run endpoints.

- You can run **pipenv shell** in order to activate your virtual environment.
- Install dependencies with **pipenv install** which are defined in **Pipfile** document.
- The package **opencv-python** in Linux environments will make you install dependencies on your system, so you need to install **opencv-python-headless** instead.
- Finally, run the service with **uvicorn main:app --reload --env-file=.env**.
- The .env file contains your **connection string**. You can get it from your Azure storage account in the left menu, "Access keys". In the right side you can see that data hidden. Press the "Show" button and copy that connection string into your .env file.
  <br></br>
<img src="pic1.png" width="650" height="400" />
  <br>
- Don't forget to install **python-dotenv** package and not **dotenv** packege only. This allow you to use your environment variables with the getenv function. Use https://pypi.org to know the exact command to install the desired package. If you type in your browser "dotenv pypi" you'll see the results showing the url for the pypi website with tha package name.


## How to handle endpoints.
- Once your server is running with Uvicorn you'll see that it's running in http://127.0.0.1:8000.
- Add **/docs** at the end of the URL to open the Swagger interactive API documentation where you can test your functions and debug any detail.
