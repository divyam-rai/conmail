import os
import glob
import constants as cst
import shutil

if not os.path.exists(cst.PROTOC_TARGET_FOLDER):
    os.makedirs(cst.PROTOC_TARGET_FOLDER)

# Generate python stubs using protoc.
command = f"python -m grpc_tools.protoc \
    -I{cst.INPUT_FOLDER} \
    --python_out={cst.PROTOC_TARGET_FOLDER} \
    --pyi_out={cst.PROTOC_TARGET_FOLDER}"

for file in glob.glob(f"{cst.INPUT_FOLDER}/" + '**/*.proto', recursive=True):
    os.system(f"{command} {file}")

# Build package.
with open(f"{cst.PROTOC_TARGET_FOLDER}/pyproject.toml", 'w+') as f:
   f.write(cst.PACKAGE_META)

os.system(f"python -m build {cst.PROTOC_TARGET_FOLDER}")

shutil.copytree(f"{cst.PROTOC_TARGET_FOLDER}/dist", cst.DIST_FOLDER, dirs_exist_ok=True)
shutil.rmtree(os.path.join(f"{cst.PROTOC_TARGET_FOLDER}"))