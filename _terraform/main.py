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
    name = "Terraform_Winterfun"
  }
}
}

provider "aws" {
  profile = "default"
  region  = "eu-west-1"
}


#dev instance creation
resource "aws_instance" "dev_winterfun" {
  ami           = "ami-08ca3fed11864d6bb"
  instance_type = "t3.medium"
  subnet_id     = "subnet-065588da7b835f2b9"
  associate_public_ip_address = true
  key_name = "x21126151_wislan_lima_new"
  vpc_security_group_ids = ["sg-0f18d077b96cfd4fe"]

  tags = {
    Name = "dev_winterfun"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.pvt_key
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
resource "aws_instance" "stage_winterfun" {
  ami           = "ami-08ca3fed11864d6bb"
  instance_type = "t3.medium"
  subnet_id     = "subnet-065588da7b835f2b9"
  associate_public_ip_address = true
  key_name = "x21126151_wislan_lima_new"
  vpc_security_group_ids = ["sg-0f18d077b96cfd4fe"]

  tags = {
    Name = "stage_winterfun"
  }


  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.pvt_key
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
resource "aws_instance" "prod_winterfun" {
  ami           = "ami-08ca3fed11864d6bb"
  instance_type = "t3.medium"
  subnet_id     = "subnet-065588da7b835f2b9"
  associate_public_ip_address = true
  key_name = "x21126151_wislan_lima_new"
  vpc_security_group_ids = ["sg-0f18d077b96cfd4fe"]

  tags = {
    Name = "prod_winterfun"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.pvt_key
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


#sonarcube instance creation
resource "aws_instance" "sonarqube_winterfun" {
  ami           = "ami-08ca3fed11864d6bb"
  instance_type = "t3.medium"
  subnet_id     = "subnet-065588da7b835f2b9"
  associate_public_ip_address = true
  key_name = "x21126151_wislan_lima_new"
  vpc_security_group_ids = ["sg-0f18d077b96cfd4fe"]

  tags = {
    Name = "sonarqube_winterfun"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.pvt_key
    }

  # copies file from local directory to remote directory
  provisioner "file" {
    source      = "docker_compose_install_sonarqube.sh"
    destination = "/tmp/docker_compose_install_sonarqube.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/docker_compose_install_sonarqube.sh",
      "/tmp/docker_compose_install_sonarqube.sh",
    ]
  }
}

#sonarcube instance creation
resource "aws_instance" "elk_stack_winterfun" {
  ami           = "ami-08ca3fed11864d6bb"
  instance_type = "t3.medium"
  subnet_id     = "subnet-065588da7b835f2b9"
  associate_public_ip_address = true
  key_name = "x21126151_wislan_lima_new"
  vpc_security_group_ids = ["sg-0f18d077b96cfd4fe"]

  tags = {
    Name = "elk_stack_winterfun"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = var.pvt_key
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
output "prod_winterfun"{
value = "${aws_instance.prod_winterfun.public_ip}"
}

output "dev_winterfun"{
value = "${aws_instance.dev_winterfun.public_ip}"
}

output "stage_winterfun"{
value = "${aws_instance.stage_winterfun.public_ip}"
}

output "sonarqube_winterfun"{
value = "${aws_instance.sonarqube_winterfun.public_ip}"
}

output "elk_stack_winterfun"{
value = "${aws_instance.elk_stack_winterfun.public_ip}"
}
