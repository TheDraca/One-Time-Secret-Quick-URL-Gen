#!/bin/bash

#Create directory and copy needed files
mkdir -p $HOME/.ots
cp ots.pyw $HOME/.ots/
cp JsonControl.py $HOME/.ots/

#Test if we already have a  json file
if test -f "$HOME/.ots/OTS.json"; then
    echo "WARNING: You already have OTS.json file watch out if there have been any changes to the file"
fi

#Check if theres a ZSH rc file
if test -f "$HOME/.zshrc"; then
    if ! grep -q "alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)'" $HOME/.zshrc ; then
        echo "ZSH RC File found but alias not setup, creating ots alias now"
        echo "alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)'" >> $HOME/.zshrc
    fi
#Check if we don't have a bash profile OR a zsh profile and warn about it
else ! test -f "$HOME/.bash_profile"
    echo "No ZSH File or bash profile, guessing you are using bash and putting the alias in a new bash_profile"
    touch "$HOME/.bash_profile"
fi

#If there's a bash profile file add alias to it
if test -f "$HOME/.bash_profile"; then
    if ! grep -q "alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)'" $HOME/.bash_profile ; then
        echo "Bash RC File found but alias not setup, creating ots alias now"
        echo "alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)'" >> $HOME/.bash_profile
    fi
fi


echo "OTS should now been installed to $HOME/.ots"
echo "You may now delete these files, you may need to restart your terminal before the ots command works, if it doesn't add this alias to whatever shell you use:
alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)' "
