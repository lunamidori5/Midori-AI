import os
import sys
import json
import time
import base64
import shutil
import hashlib
import tarfile
import zipfile
import getpass
import pathlib
import platform
import argparse
import subprocess

from halo import Halo

from rich import print
from rich.text import Text
from rich.tree import Tree
from rich.markup import escape
from rich.console import Console
from rich.prompt import Confirm
from rich.filesize import decimal

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM