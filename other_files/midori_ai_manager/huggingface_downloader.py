import argparse
import requests

def download_file_from_url(url, filename, username, reponame, modeltype):
    """
    Download the file from the given URL to the given file 

    Args:
    url: The URL of the file to download.
    filename: The name of the file to save the downloaded file to.
    username: The username for the Hugging Face account.
    reponame: The name of the Hugging Face repository to download the model from.
    modeltype: The name of the model to download.
    """

    headers = {
        'username': username,
        'reponame': reponame,
        'modeltype': modeltype
    }

    r = requests.get(url, headers=headers, allow_redirects=True)
    open(filename, 'wb').write(r.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True, help="The URL of the file to download.")
    parser.add_argument("--username", type=str, required=True, help="The username for the Hugging Face account.")
    parser.add_argument("--reponame", type=str, required=True, help="The name of the Hugging Face repository to download the model from.")
    parser.add_argument("--modeltype", type=str, required=True, help="The name of the model to download.")
    args = parser.parse_args()


    url = args.url
    filename = args.filename
    username = args.username
    reponame = args.reponame
    modeltype = args.modeltype

    # Download the file
    download_file_from_url(url, filename, username, reponame, modeltype)