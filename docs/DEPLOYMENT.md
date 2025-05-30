# Task: Write brief answers (1-2 paragraphs each) to these two basic questions:


## What approach would you use to version and track different models in production?

In a pure git-based workflow, I would use git tags to manage release versions of the model, its underlying training code, and data-files.
However, I know a model registry would be *much* better for production environments, where I have read Databricks (with mlflow) is a good option. (https://docs.databricks.com/aws/en/machine-learning/mlops/ci-cd-for-ml)


## What key metrics would you monitor for this API service and the prediction model?

For the API Service, I would use Datadog to monitor standard API metrics like response time, errors and number of unsuccessful requests. For the prediction model, I could monitor the model's accuracy on incoming requests, and see how it performs over time.