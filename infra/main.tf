terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_vpc" "release_guard_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "release-guard-vpc"
  }
}

resource "aws_subnet" "release_guard_public_subnet" {
  vpc_id                  = aws_vpc.release_guard_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "release-guard-public-subnet"
  }
}

resource "aws_internet_gateway" "release_guard_igw" {
  vpc_id = aws_vpc.release_guard_vpc.id

  tags = {
    Name = "release-guard-igw"
  }
}
resource "aws_route_table" "release_guard_public_rt" {
  vpc_id = aws_vpc.release_guard_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.release_guard_igw.id
  }

  tags = {
    Name = "release-guard-public-rt"
  }
}
resource "aws_route_table_association" "release_guard_public_rt_assoc" {
  subnet_id      = aws_subnet.release_guard_public_subnet.id
  route_table_id = aws_route_table.release_guard_public_rt.id
}
resource "aws_security_group" "release_guard_sg" {
  name        = "release-guard-sg"
  description = "Security group for Release Guard EC2"
  vpc_id      = aws_vpc.release_guard_vpc.id

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "release-guard-sg"
  }
}
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
resource "aws_instance" "release_guard_ec2_v2" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.release_guard_public_subnet.id
  vpc_security_group_ids       = [aws_security_group.release_guard_sg.id]
  key_name                    = "release-guard-key"
  associate_public_ip_address = true

  tags = {
    Name = "release-guard-ec2"
  }
}
