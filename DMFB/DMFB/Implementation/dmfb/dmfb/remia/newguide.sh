sed -i 's/, dropletIdList//g' remi.txt
dist=$1

grep DropletDispense remi.txt | sed 's/(//g' | sed 's/)//g' | sed 's/\[//g' | sed 's/\]//g' | sed 's/ //g' | awk -F ',' '{for(i=4;i<=NF;i++) print "a_"$2"_"$3"_[0-9]*_"$i" = True"}' > temp
rm temp2
rm temp3
cat temp | while read line ; do grep "$line" op_correct >> temp2; done
#cat temp2 | while read line ; do if ! grep -q "$line" op; then  echo $line >> temp3; fi; done

grep enforceMixing remi.txt | sed 's/(//g' | sed 's/)//g' | sed 's/\[//g' | sed 's/\]//g' | sed 's/ //g' | awk -F ',' '{for(i=0;i<=1;i++) if(i ==1)print "a_"$2"_"$3"_[0-9]*_"$6" = True"; else print "a_"$4"_"$5"_[0-9]*_"$6" = True";}' > temp
cat temp | while read line ; do grep "$line" op_correct >> temp2; done
#cat temp2 | while read line ; do if ! grep -q "$line" op; then  echo $line >> temp3; fi; done


grep DropletDisappearence remi.txt | sed 's/(//g' | sed 's/)//g' | sed 's/\[//g' | sed 's/\]//g' | sed 's/ //g' | awk -F ',' '{for(i=4;i<=NF;i++) print "a_"$2"_"$3"_[0-9]*_"$i-1" = True"}' > temp
cat temp | while read line ; do grep "$line" op_correct >> temp2; done
cat temp2 | while read line ; do if ! grep -q "$line" op; then  echo $line >> temp3; fi; done
cat temp3 | sed 's/ = True//g' | sed 's/_/ /g' | sort -nk 5 > prob.dat
cat temp2 | sed 's/ = True//g' | sed 's/_/ /g' | sort -nk 5 > mile.dat

rm t2
rm t1
rm t
rm p.dat
less prob.dat | awk '{print $4}' | sort -u > d
for d in `cat d`; do grep "a [0-9]* [0-9]* $d [0-9]*" prob.dat | sort -u -k5 | head -1 >> p.dat; done

cat p.dat | while read a x y d t; do grep "a [0-9]* [0-9]* "$d" [0-9]*" mile.dat | grep -B 1 "a [0-9]* [0-9]* "$d" "$t"$" | head -n 1 | while read ab xb yb db tb; do echo "$d at $t till $tb"; grep "a_[0-9]*_[0-9]*_"$d"_[0-9]* = True" op_correct | sed 's/ = True//g' | sed 's/_/ /g' | sort -nk 5 -r | sed -n "/a [0-9]* [0-9]* "$d" "$t"$/,/a [0-9]* [0-9]* "$d" "$tb"$/p"> t; grep "a_[0-9]*_[0-9]*_"$d"_[0-9]* = True" op | sed 's/ = True//g' | sed 's/_/ /g' | sort -nk 5 -r | sed -n "/a [0-9]* [0-9]* "$d" "$t"$/,/a [0-9]* [0-9]* "$d" "$tb"$/p"> t1; done; echo "$d at" >> t2; cat t | while read ab xb yb db tb; do if ! grep -q ""$ab" "$xb" "$yb" "$db" "$tb"" t1; then echo "$(cat t2) $tb" > t2; fi; done; done

if cmp -s t2 t2bkp
then
  echo "detected same t2"
  if [ "$dist" -gt 1 ] 
   then
          let dist-- #="$dist"-1
fi
else
  if [ "$dist" -lt "$1" ]
  then
  let dist++ #="$dist"+1
fi
fi   
echo "distance is $dist"

cp t2 t2bkp

cat t2

#awk -v x=$dist '{for(i=NF;i>2;i=i-x) print $1" "$(i)}' t2 | while read d t; do grep "a_[0-9]*_[0-9]*_"$d"_"$t" = True" op_correct | sed 's/ = True//g' | sed 's/_/ /g' | awk '{print $2","$3","$5}' >> cplist.txt; done
awk '{if(NF != 3) print $1" "$(NF); else print $1" "$3}' t2 | while read d t; do grep "a_[0-9]*_[0-9]*_"$d"_"$t" = True" op_correct | sed 's/ = True//g' | sed 's/_/ /g' | awk '{print $2","$3","$5}' >> cplist.txt; done

cat cplist.txt | sort -u > cplist2.txt
cp cplist2.txt cplist.txt
#cat cplist.txt
