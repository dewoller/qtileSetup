#!/bin/sh
date >>/tmp/qshell
echo $1 >>/tmp/qshell
echo $1 | qshell
