#!/bin/bash
CHALNAME="Script Name"
SCRIPT="Script Name.py"
CHALDIR="$(pwd)/"
ABASENAME="kali-autopilot_attack_"
MUTEXAPI="mutex-api.py"
ASERVICE=$ABASENAME$CHALNAME
AEXECSTART="$CHALDIR$SCRIPT"
SSL_CERT="./Script Name.cert"
SSL_PRIV_KEY="./kali-autopilot.key"
function check_root(){
    if [[ $EUID -ne 0 ]]; then
        printf "\n$(basename $0) must be run as root.\ntry: sudo ./$(basename $0)\n\n"
        exit 1
    fi
}
function print_usage() {
    cat << EOF

usage: sudo ./service.sh <option>
 This will set up Kali-Autopilot services
 OPTIONS:
    -c        Create SSL certificates
    -d        Debug attack service
    -h        Show this message
    -i        Install and start attack service
    -r        Stop and remove attack service
    -s        Show service status
EOF
}
function create_ssl_certs() {
    openssl genrsa -out $SSL_PRIV_KEY 2048
    openssl req -new -x509 -days 1095 -key $SSL_PRIV_KEY -out $SSL_CERT 
}
function debug_attack_service() {
    journalctl --output cat -fu $ASERVICE
}
function show_status() {
    systemctl status $ASERVICE
}
function remove_attack_service() {
    check_root

    systemctl disable $ASERVICE --now >/dev/null 2>&1
    rm -f /etc/systemd/system/$ASERVICE.service >/dev/null 2>&1
        printf "\nService removed\n\n"
}
function install_attack_service {
    check_root

    cat << EOF >> /etc/systemd/system/$ASERVICE.service
[Unit]
Description=This service executes Kali-Autopilot attack scripts
ConditionPathExists=$AEXECSTART


[Service]
ExecStart=/usr/bin/env python3 $AEXECSTART
WorkingDirectory=$CHALDIR
Restart=always
RestartSec=30


[Install]
WantedBy=multi-user.target
EOF

systemctl enable $ASERVICE --now
printf "\nService $ASERVICE installed\n\n"
}
while getopts "cdhirs" opt; do
  case "$opt" in
  c)  create_ssl_certs
      exit 0
      ;;
  d)  debug_attack_service
      exit 0
      ;;
  h)  print_usage
      exit 0
      ;;
  i)  install_attack_service
      exit 0
      ;;
  r)  remove_attack_service
      exit 0
      ;;
  s)  show_status
      exit 0
      ;;
  \?) print_usage
      exit 1
      ;;
  esac
done

print_usage
