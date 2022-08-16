#!/usr/bin/env bash

# cd "$(dirname "$0")"
if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="wine-quality-prediction:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    docker build -t ${LOCAL_IMAGE_NAME} ..
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi

docker-compose up -d

sleep 5

export AWS_DEFAULT_REGION=ap-south-1
export AWS_ACCESS_KEY_ID="abc"
export AWS_SECRET_ACCESS_KEY="xyz"

aws s3 mb s3://red-wine-quality --endpoint-url=http://localhost:4566

# check whether s3 bucket is created or not
aws s3 ls --endpoint-url http://localhost:4566

export INPUT_FILE_PATTERN="s3://red-wine-quality/in/red_wine_train.csv"
export OUTPUT_FILE_PATTERN="s3://red-wine-quality/out/predictions.csv"
export S3_ENDPOINT="http://localhost:4566"

pipenv run python integration_test.py

# verify input file
aws s3 ls s3://red-wine-quality/in/ --endpoint-url=http://localhost:4566

# verify output file
aws s3 ls s3://red-wine-quality/out/ --endpoint-url=http://localhost:4566

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down
