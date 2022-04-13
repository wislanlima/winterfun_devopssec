terraform {

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
    cloud {
  organization = "NCI2022PROJECT"
  workspaces {
    name = "TF_WINTERFUN"
  }
}
}



provider "aws" {
  profile = "default"
  region  = "eu-west-1"
}


#dev instance creation
resource "aws_instance" "x21126151_Wislan_Lima_dev" {
  ami           = "ami-08ca3fed11864d6bb"
  instance_type = "t2.medium"
  subnet_id     = "subnet-065588da7b835f2b9"
  associate_public_ip_address = true
  key_name = "x21126151_Wislan_Lima"
  vpc_security_group_ids = ["sg-0f18d077b96cfd4fe"]

  tags = {
    Name = "x21126151_Wislan_Lima_dev"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    agent = false
    private_key = var.PVT_KEY
    }



  # copies file from local directory to remote directory
  provisioner "file" {
    source      = "docker_compose_install.sh"
    destination = "/tmp/docker_compose_install.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/docker_compose_install.sh",
      "/tmp/docker_compose_install.sh",
    ]

  }

}

#stage instance creation
resource "aws_instance" "x21126151_Wislan_Lima_stage" {
  ami           = "ami-08ca3fed11864d6bb"
  instance_type = "t2.medium"
  subnet_id     = "subnet-065588da7b835f2b9"
  associate_public_ip_address = true
  key_name = "x21126151_Wislan_Lima"
  vpc_security_group_ids = ["sg-0f18d077b96cfd4fe"]

  tags = {
    Name = "x21126151_Wislan_Lima_stage"
  }


  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.PVT_KEY
    }

  # copies file from local directory to remote directory
  provisioner "file" {
    source      = "docker_compose_install.sh"
    destination = "/tmp/docker_compose_install.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/docker_compose_install.sh",
      "/tmp/docker_compose_install.sh",
    ]

  }

}


#prod instance creation
resource "aws_instance" "x21126151_Wislan_Lima_prod" {
  ami           = "ami-08ca3fed11864d6bb"
  instance_type = "t2.medium"
  subnet_id     = "subnet-065588da7b835f2b9"
  associate_public_ip_address = true
  key_name = "x21126151_Wislan_Lima"
  vpc_security_group_ids = ["sg-0f18d077b96cfd4fe"]

  tags = {
    Name = "x21126151_Wislan_Lima_prod"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.PVT_KEY
    }

  # copies file from local directory to remote directory
  provisioner "file" {
    source      = "docker_compose_install.sh"
    destination = "/tmp/docker_compose_install.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/docker_compose_install.sh",
      "/tmp/docker_compose_install.sh",
    ]

  }

}

#IP of instances retrieved
output "x21126151_Wislan_Lima_prod"{
value = "${aws_instance.x21126151_Wislan_Lima_prod.public_ip}"
}

output "x21126151_Wislan_Lima_dev"{
value = "${aws_instance.x21126151_Wislan_Lima_dev.public_ip}"
}

output "x21126151_Wislan_Lima_stage"{
value = "${aws_instance.x21126151_Wislan_Lima_stage.public_ip}"
}
