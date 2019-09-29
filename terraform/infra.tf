# Provider Block
provider "aws" {
  version    = "~> 2.7"
  region     = "ap-southeast-1"
}

resource "aws_s3_bucket" "pycon_random_bucket" {
  acl    = "private"
  force_destroy = true
  region     = "ap-southeast-1"

  versioning {
    enabled = false
  }

}

resource "aws_ssm_parameter" "s3bucket_keys" {
  type  = "String"
  name  = "/pycon/random-bucket"
  value = "${aws_s3_bucket.pycon_random_bucket.bucket}"
  overwrite = true
}

resource "aws_ssm_parameter" "random_env_var" {
  type  = "String"
  name  = "/pycon/random-var"
  value = "random_variable"
  overwrite = true
}

resource "aws_s3_bucket_object" "object_10MB" {
  bucket = "${aws_s3_bucket.pycon_random_bucket.bucket}"
  key    = "10.txt"
  source = "files/10.txt"
}

resource "aws_s3_bucket_object" "object_100MB" {
  bucket = "${aws_s3_bucket.pycon_random_bucket.bucket}"
  key    = "100.txt"
  source = "files/100.txt"
}

resource "aws_s3_bucket_object" "object_256MB" {
  bucket = "${aws_s3_bucket.pycon_random_bucket.bucket}"
  key    = "256.txt"
  source = "files/256.txt"
}

resource "aws_s3_bucket_object" "object_512MB" {
  bucket = "${aws_s3_bucket.pycon_random_bucket.bucket}"
  key    = "512.txt"
  source = "files/512.txt"
}

resource "aws_s3_bucket_object" "object_1024MB" {
  bucket = "${aws_s3_bucket.pycon_random_bucket.bucket}"
  key    = "1024.txt"
  source = "files/1024.txt"
}

resource "aws_s3_bucket_object" "shodan_results" {
  bucket = "${aws_s3_bucket.pycon_random_bucket.bucket}"
  key    = "shodan-export.json.gz"
  source = "files/shodan-export.json.gz"
}

resource "aws_s3_bucket_object" "config" {
  bucket = "${aws_s3_bucket.pycon_random_bucket.bucket}"
  key    = "config.json"
  source = "files/config.json"
}


