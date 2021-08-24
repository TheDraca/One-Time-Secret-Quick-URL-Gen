#!/bin/bash
mkdir -p $HOME/.ots
cp ots.pyw $HOME/.ots/
cp JsonControl.py $HOME/.ots/
cp OTS.json $HOME/.ots/

#Check if theres a ZSH rc file
if test -f "$HOME/.zshrc"; then
    if ! grep -q "alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)'" $HOME/.zshrc ; then
        echo "ZSH RC File found but alias not setup, creating ots alias now"
        echo "alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)'" >> $HOME/.zshrc
    fi
else ! test -f "$HOME/.bash_profile"
    echo "No ZSH File or bash profile, guessing you are using bash and putting the alisa there"
    touch "$HOME/.bash_profile"
fi

#Check if there's a bash profile file add alias to it
if test -f "$HOME/.bash_profile"; then
    if ! grep -q "alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)'" $HOME/.bash_profile ; then
        echo "Bash RC File found but alias not setup, creating ots alias now"
        echo "alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)'" >> $HOME/.bash_profile
    fi
fi


echo "OTS should now been installed to $HOME/.ots"
echo "You may now delete these files, you may need to restart your terminal before the ots commanded works. If it doesn't add this alias to whatever shell you use:
alias ots='(cd $HOME/.ots && python3 ots.pyw && cd - > /dev/null)' "
