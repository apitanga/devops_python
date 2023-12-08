# Python script to generate a basic Terraform configuration file

config_template = """
provider "aws" {{
  region = "{region}"
}}

resource "aws_instance" "example" {{
  ami           = "{ami}"
  instance_type = "t2.micro"
}}
"""

def generate_terraform_config(region, ami):
    """
    Generates a Terraform configuration with the specified region and AMI.
    """
    config = config_template.format(region=region, ami=ami)
    with open('main.tf', 'w') as file:
        file.write(config)
    print("Terraform configuration file 'main.tf' created.")

# Example usage
generate_terraform_config('us-west-1', 'ami-abc1234')
