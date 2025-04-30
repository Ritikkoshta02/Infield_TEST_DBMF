file=$1
#size=$2
a="sat"
rm cplist.txt
touch cplist.txt
i=0
start=`date +%s`
#less "$1".txt | sed 's/(//g' | sed 's/)//g' | sed 's/ *//g' | sed 's/,dropletIdList//g' > mix.txt
#less op_correct | grep " = True" |  sed 's/ = True//g' | sed 's/_/ /g' | sort -nk 5 > golden.txt
#python try.py > log

#cp newcplist.txt cplist.txt

while [ "$a" == "sat" ]
do
i=$(($i+1))
echo "trial next"
python "$file".py > res
#cat res | head -n 1 | read a 
a=$(cat "res" | head -n 1)
if [ "$a" == "sat" ] 
then
bash guide.sh "$file"
fi
echo "$a"
done
#i=$i-1
end=`date +%s`
i=$(($i-1))
runtime=$((end-start))
echo "$runtime"
echo "number of iter"
echo $i

echo "in the cplist"
less cplist.txt | wc -l

echo "unique time steps"
less cplist.txt | sed 's/,/ /g' | awk '{print $3}' | sort -u | wc -l
#python display8.py
#cp -f Biochip.pdf /mnt/c/Users/mos28/Documents/research/reversible/biochip/verification/
