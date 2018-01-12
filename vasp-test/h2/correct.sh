for files in `/bin/ls $RUNNAME*xsf`; do
oldx1=`cat $files | grep -A2 'BEGIN_DATAGRID' | tail -1 | awk '{ print $1 }'`
cell1=`cat $files | grep -A1 'CONVVEC' | tail -1 | awk '{ print $1 }'`
newx1=`echo $oldx1+$cell1 | bc -l`
oldx2=`cat $files | grep -A2 'BEGIN_DATAGRID' | tail -1 | awk '{ print $2 }'`
cell2=`cat $files | grep -A2 'CONVVEC' | tail -1 | awk '{ print $2 }'`
newx2=`echo $oldx1+$cell1 | bc -l`
oldx3=`cat $files | grep -A2 'BEGIN_DATAGRID' | tail -1 | awk '{ print $3 }'`
cell3=`cat $files | grep -A3 'CONVVEC' | tail -1 | awk '{ print $3 }'`
newx3=`echo $oldx1+$cell1 | bc -l`
cat $files | sed 's/'$oldx1'/'$newx1'/g' >> $files.2
cat $files.2 | sed 's/'$oldx2'/'$newx2'/g' >> $files.3
cat $files.3 | sed 's/'$oldx3'/'$newx3'/g' >> $files.4
rm -f $files.2
rm -f $files.3
mv -f $files.4 $spin$files
done