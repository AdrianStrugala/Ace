import os
os.chdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import sys
sys.path.insert(0, os.getcwd())
from setup.settings import hparams, preprocessing
import errno
import shutil
import time
import colorama
import zipfile

original_cwd = os.getcwd()


colorama.init()


MAX = 99*1024*1024         # 99 Mb    - max chapter size
BUF = 6*1024*1024*1024    # 6GB     - memory buffer size


def file_split(FILE, MAX):
    '''Split file into pieces, every size is  MAX = 15*1024*1024 Byte'''
    chapters = 1
    uglybuf = ''
    with open(FILE, 'rb') as src:
        while True:
            tgt = open(FILE + '.%03d' % chapters, 'wb')
            written = 0
            while written < MAX:
                if len(uglybuf) > 0:
                    tgt.write(uglybuf)
                tgt.write(src.read(min(BUF, MAX - written)))
                written += min(BUF, MAX - written)
                uglybuf = src.read(1)
                if len(uglybuf) == 0:
                    break
            tgt.close()
            if len(uglybuf) == 0:
                break
            chapters += 1


# Copy file or folder recursively
def copy(path):

    print('{}Copying:{} {}'.format(colorama.Fore.GREEN, colorama.Fore.RESET, path))

    while True:
        try:

            # If it's file - copy it
            if os.path.isfile(path):

                # Create folder(s) first
                try:
                    os.mkdir(os.path.dirname('_deployment/' + path))
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise

                # Copy file
                shutil.copy2(path, '_deployment/' + path)

            # Folder - copy it's content recursively
            else:
                shutil.copytree(path, '_deployment/' + path, ignore=copy_ignore)

        # In case of error sleep for a while, print error mesage and retry
        except Exception as e:
            print("{}{}{}".format(colorama.Fore.RED, str(e), colorama.Fore.RESET))
            time.sleep(1)
            continue
        return

# Filter function for folder copy (prints filenames and returns list of files/folders to ignore)
def copy_ignore(path, content):

    blacklist = [path for path in content if path.startswith('.git') or path == '__pycache__']
    print('\n'.join(['{}Copying:{} {}/{}'.format(colorama.Fore.GREEN, colorama.Fore.RESET, path, file) for file in content if file not in blacklist]))
    return blacklist

# Find all available checkpoints
checkpoints = [file[:-6] for file in os.listdir(hparams['out_dir']) if os.path.isfile(hparams['out_dir'] + file) and file[-6:] == '.index']

# If there are no any - print error message and quit
if not checkpoints:
    print('{}There are no model checkpoints ready for deployment{}'.format(colorama.Fore.RED, colorama.Fore.RESET))
    sys.exit()

# Read default checkpoint for model
try:
    default_checkpoint = open(hparams['out_dir'] + 'checkpoint').readline()
except:
    default_checkpoint = ''

# Create deployment folder - wrror if folder exists
try:
    os.makedirs(os.getcwd() + '/_deployment')
except OSError as e:
    if e.errno == errno.EEXIST:
        print('{}Deployment folder already exists, (re)move it to continue{}'.format(colorama.Fore.RED, colorama.Fore.RESET))
        sys.exit()
    else:
        raise

# Print list of checkpoints
default_index = len(checkpoints)
print("\n\n{}List of available checkpoints:{}".format(colorama.Fore.GREEN, colorama.Fore.RESET))
for index, checkpoint in enumerate(checkpoints):
    print("{}{}.{} {}{}".format(colorama.Fore.GREEN, index + 1, colorama.Fore.RESET, '*' if checkpoint in default_checkpoint else '', checkpoint))
    if checkpoint in default_checkpoint:
        default_index = index + 1


choice = default_index

# Static list of files to be copied for any settings
paths = ['core',
         'nmt',
         'setup',
         'utils',
         'inference.py',
         'train.py',
         hparams['out_dir'] + 'hparams']

# Append source vocab
paths.append(hparams['vocab_prefix'] + '.' + hparams['src'])

# Append target vocab (if shared vocab is not set)
if not hparams['share_vocab']:
    paths.append(hparams['vocab_prefix'] + '.' + hparams['tgt'])

# If model is using our BPE/WPM-like tokenizer
if preprocessing['use_bpe']:

    # And shared vocab - copy json file with list of joins
    if hparams['share_vocab']:
        paths.append(preprocessing['train_folder'] + 'bpe_joins.common.json')

    # Else copy source and target files as above
    else:
        paths.append(preprocessing['train_folder'] + 'bpe_joins.{}.json'.format(hparams['src']))
        paths.append(preprocessing['train_folder'] + 'bpe_joins.{}.json'.format(hparams['tgt']))

    # Protected phrases for BPE/WMP-like tokenizer
    paths.append('setup/protected_phrases_bpe.txt')

else:

    # Protected phrases for standard tokenizer
    paths.append('setup/protected_phrases_standard.txt')

# Append rules for standard tokenizer if used
if not preprocessing['embedded_detokenizer']:
    paths.append('setup/answers_detokenize.txt')

# Finally append choosen model files
paths.extend([hparams['out_dir'] + file for file in os.listdir(hparams['out_dir']) if file.startswith(checkpoints[choice - 1])])

# Copy all files
[copy(path) for path in paths]

# Write checkpoint file for TensorFlow with choosen model
print('{}Writing:{} {}checkpoint'.format(colorama.Fore.GREEN, colorama.Fore.RESET, hparams['out_dir']))
while True:
    try:
        with open('_deployment/' + hparams['out_dir'] + 'checkpoint', 'w', encoding='utf-8', newline='') as checkpoint_file:
            checkpoint_file.write('model_checkpoint_path: "{}"'.format(checkpoints[choice - 1]))
    except Exception as e:
        print("{}{}{}".format(colorama.Fore.RED, str(e), colorama.Fore.RESET))
        time.sleep(1)
        continue
    break

# Create best_bleu folder (necessary)
print('{}Creating:{} {}best_bleu/checkpoint'.format(colorama.Fore.GREEN, colorama.Fore.RESET, hparams['out_dir']))
while True:
    try:
        os.mkdir('_deployment/' + hparams['out_dir'] + 'best_bleu')
    except Exception as e:
        if e.errno != errno.EEXIST:
            print("{}{}{}".format(colorama.Fore.RED, str(e), colorama.Fore.RESET))
            time.sleep(1)
            continue
    break


# Zip checkpoint file - it is bigger than 100Mb
os.chdir(os.path.dirname(os.path.realpath(__file__)) + '\_deployment\model')

#Find the bigest file in model folder
biggest = ("", -1)
dir = str(os.getcwd())
for item in os.listdir(dir):
    item = dir + "/" + item

    itemsize = os.path.getsize(item)
    if itemsize > biggest[1]:
            biggest = (item, itemsize)

#Set up zip name
zip_name = str(biggest[0] + '.zip')

# writing files to a zipfile
with zipfile.ZipFile(zip_name, 'w') as zip:
    zip.write(biggest[0])

# splitting zip into partitions
file_split(zip_name, MAX)

print('Zipps created successfully!')

#remove files too big to be deployed
os.remove(biggest[0])
print('\n{}Removed: {}{}\n\n'.format(colorama.Fore.RED, biggest[0], colorama.Fore.RESET))
os.remove(zip_name)
print('\n{}Removed: {}{}\n\n'.format(colorama.Fore.RED, zip_name, colorama.Fore.RESET))

os.chdir(original_cwd)
print('\n{}Done. You can find deployment-ready copy of chatbot in _deployment folder{}\n\n'.format(colorama.Fore.GREEN, colorama.Fore.RESET))