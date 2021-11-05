#!/bin/bash

rm -rf sources
rm -rf assembled

mkdir sources
mkdir assembled

for row in $(cat sources.json | jq -rc '.[]'); do
    _jq() {
        echo "${row}" | jq -r "${1}"
    }

    rid=$(_jq '.rid')
    rlink=$(_jq '.rlink')
    yrl=$(_jq '.yrl')

    git clone "$rlink" sources/"$rid"

    find sources/"$rid"/"$yrl" -name "*.yar" -o -name "*.yara" -type f | while read fname; do
        echo "$fname"
        cat "$fname" >> assembled/$rid.yar
    done
done
