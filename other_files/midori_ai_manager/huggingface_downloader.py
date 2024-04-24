import time
import argparse
import requests

def download_file_from_midori_ai(url, filename, username, reponame, modeltype):
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

    for i in range(15):
        try:
            r = requests.get(url, headers=headers, allow_redirects=True)
            open(filename, 'wb').write(r.content)
            return
        except:
            print(f"Retrying download in 2 seconds... Attempt {i + 1}/15")
            time.sleep(2)
    raise Exception("Failed to download file after 15 retries.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-un", "--username", type=str, required=True, help="The username for the Hugging Face account.")
    parser.add_argument("-r", "--reponame", type=str, required=True, help="The name of the Hugging Face repository to download the model from.")
    parser.add_argument("-m", "--modeltype", type=str, required=True, help="The name of the model to download.")
    args = parser.parse_args()

    filename = args.modeltype
    username = args.username
    reponame = args.reponame
    modeltype = args.modeltype
    url = f"https://tea-cup.midori-ai.xyz/huggingface/model/{modeltype}"

    # Download the file
    download_file_from_midori_ai(url, filename, username, reponame, modeltype)