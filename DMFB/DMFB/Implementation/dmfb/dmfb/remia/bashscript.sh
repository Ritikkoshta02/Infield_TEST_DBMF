file=$1
#size=$2
a="sat"
start=`date +%s`
#rm newcplist.txt
#less remi.txt | sed 's/(//g' | sed 's/)//g' | sed 's/ *//g' > remimix.txt
#less op_correct | grep " = True" |  sed 's/ = True//g' | sed 's/_/ /g' | sort -nk 5 > remi_golden.txt
#python try.py > log

#cp newcplist.txt cplist.txt
rm cplist.txt
touch cplist.txt
while [ "$a" == "sat" ]
do
echo "trial next"
python $file > res
#cat res | head -n 1 | read a 
a=$(cat "res" | head -n 1)
if [ "$a" == "sat" ] 
then
bash guide.sh 
fi
echo "$a"
done

end=`date +%s`
#i=$(($i-1))
runtime=$((end-start))
echo "$runtime"
#python display8.py
#cp -f Biochip.pdf /mnt/c/Users/mos28/Documents/research/reversible/biochip/verification/
