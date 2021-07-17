# carton-labels
Carton-labels AWS Lambdas Repo

1. Create lambda fn from scratch
    name : {name}
    runtime : python3.8
2. Upload zip file
3. Increase the task timeout to minimum 1 min (as it is pdf genearation task)

# File to copy
1. lambda_funcation.py
2. arial.ttf

# sample request
{
  "company": "Mid Atlantic Tiger LLC",
  "made_in": "China",
  "lot_number": "2104M",
  "cartons": [
    {
      "sku": "100100G",
      "color": "Gray",
      "no_of_cartons": 10
    },
    {
      "sku": "100101DG",
      "color": "Dark Gray",
      "no_of_cartons": 20
    }
  ]
}
