terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  required_version = ">= 0.14.9"
    cloud {
  organization = "NCI2022"
  workspaces {
    name = "Terraform_Winterfun"
  }
}
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}


#dev instance creation
resource "aws_instance" "winterfun_dev" {
  ami           = "ami-04505e74c0741db8d"
  instance_type = "t2.medium"
  subnet_id     = "subnet-01f7f9c5b9fc99986"
  associate_public_ip_address = true
  key_name = "x21126151_Wislan_Lima"
  vpc_security_group_ids = ["sg-0268ecbf418effd94"]

  tags = {
    Name = "winterfun_dev"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("x21126151_Wislan_Lima.pem")
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
resource "aws_instance" "winterfun_stage" {
  ami           = "ami-04505e74c0741db8d"
  instance_type = "t2.medium"
  subnet_id     = "subnet-01f7f9c5b9fc99986"
  associate_public_ip_address = true
  key_name = "x21126151_Wislan_Lima"
  vpc_security_group_ids = ["sg-0268ecbf418effd94"]

  tags = {
    Name = "winterfun_stage"
  }


  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("x21126151_Wislan_Lima.pem")
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
resource "aws_instance" "winterfun_prod" {
  ami           = "ami-04505e74c0741db8d"
  instance_type = "t2.medium"
  subnet_id     = "subnet-01f7f9c5b9fc99986"
  associate_public_ip_address = true
  key_name = "x21126151_Wislan_Lima"
  vpc_security_group_ids = ["sg-0268ecbf418effd94"]

  tags = {
    Name = "winterfun_prod"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("x21126151_Wislan_Lima.pem")
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
resource "aws_instance" "winterfun_sonarqube" {
  ami           = "ami-04505e74c0741db8d"
  instance_type = "t3.medium"
  subnet_id     = "subnet-01f7f9c5b9fc99986"
  associate_public_ip_address = true
  key_name = "x21126151_Wislan_Lima"
  vpc_security_group_ids = ["sg-0268ecbf418effd94"]

  tags = {
    Name = "winterfun_sonarqube"
  }

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("x21126151_Wislan_Lima.pem")
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
output "winterfun_prod"{
value = "${aws_instance.winterfun_prod.public_ip}"
}

output "winterfun_dev"{
value = "${aws_instance.winterfun_dev.public_ip}"
}

output "winterfun_stage"{
value = "${aws_instance.winterfun_stage.public_ip}"
}

output "winterfun_sonarqube"{
value = "${aws_instance.winterfun_sonarqube.public_ip}"
}
