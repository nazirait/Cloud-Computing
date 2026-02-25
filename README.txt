sam package --template-file sam.yaml --output-template-file packaged.yaml --resolve-s3

sam deploy --template-file packaged.yaml --stack-name <CUSTOM-NAME> --capabilities CAPABILITY_IAM

---

sam build -t sam.yaml

sam deploy --guided