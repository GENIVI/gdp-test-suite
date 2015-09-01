#!/usr/bin/env bats 

# @test "SSH to target" {
#     run ssh -i /home/jeremiah/.ssh/id_rsa test@porter
#     [ $status -eq 0 ]
# }

# Set up test user
setup() {
    ssh-add /home/jeremiah/.ssh/id_rsa
}

@test "ssh to porter" {
    run ssh test@porter "ls -al .ssh/"
    [ ! -d "/home/test/.ssh/" ]
}

@test "NSM is active" {
    run ssh test@porter "systemctl is-active nodestatemanager-daemon.service"
    [ "$output" = "active" ]
}
