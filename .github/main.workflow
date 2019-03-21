workflow "Deploy to dockerhub on push" {
  on = "push"
  resolves = ["Push image"]
}

action "Only run on master" {
  uses = "actions/bin/filter@d820d56839906464fb7a57d1b4e1741cf5183efa"
  runs = "branch master"
}

action "Login to Docker" {
  uses = "actions/docker/login@8cdf801b322af5f369e00d85e9cf3a7122f49108"
  needs = ["Only run on master"]
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "Build image" {
  uses = "actions/docker/cli@8cdf801b322af5f369e00d85e9cf3a7122f49108"
  args = "build -t muncs/garfieldbot ."
  needs = ["Login to Docker"]
}

action "Tag as latest" {
  uses = "actions/docker/cli@8cdf801b322af5f369e00d85e9cf3a7122f49108"
  needs = ["Build image"]
  args = "tag muncs/garfieldbot muncs/garfieldbot:latest"
}

action "Push image" {
  uses = "actions/docker/cli@8cdf801b322af5f369e00d85e9cf3a7122f49108"
  needs = ["Tag as latest"]
  args = "push muncs/garfieldbot"
}
