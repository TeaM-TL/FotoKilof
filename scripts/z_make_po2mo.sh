#/bin/bash
CWD=`pwd`
NAME=fotokilof

cd ../src/locale/
for i in ??; do
    echo $i
    cd $i/LC_MESSAGES
    if [ -e $NAME.po ]; then
        msgfmt $NAME.po -o $NAME.mo
        ls $NAME*
    fi
    cd ../../
done

cd $CWD

