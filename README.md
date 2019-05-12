# kicad-bom-seeedstudio

A [KiCad](https://kicad-pcb.org) Bill-of-Materials (BOM) plugin to follow
[SeeedStudio](https://www.seedstudio.com)'s [Fusion PCBA](https://www.seeedstudio.com/fusion_pcb.html)
assembly service's [template](https://statics3.seeedstudio.com/files/20184/2018.xlsx) [Fusion PCBA Log](http://support.seeedstudio.com/knowledgebase/articles/1886734-how-do-i-prepare-the-bill-of-materials-bom-file),
that is:

```
Designator,MPN/Seeed SKU,Qty,Link
"C1,C2,C3,C4,C5", "RHA0J471MCN1GS", "5", "https://www.digikey.com.cn/product-detail/zh/nichicon/RHA0J471MCN1GS/493-3771-1-ND/2209480?keywords=RHA0J471MCN1GS"
"A1,A4", "RH0111-30002", "2", "https://statics3.seeedstudio.com/images/opl/datasheet/318020010.pdf"
"D1", "CYBLE-014008-00", "1", "https://www.digikey.com.cn/product-detail/zh/cypress-semiconductor-corp/CYBLE-014008-00/428-3600-1-ND/6052585?keywords=CYBLE-014008-00"
```

## How to use it

This plugin is set up to use the KiCad schematic's part data as it is
provided in Seeed Studio's Open Parts Library (OPL) collection for KiCad. That is:

* OPL parts have a `SKU` value defined, that's the default value to export
* If there's no `SKU`, then a `MPN` field is searched and exported
* If neither is found for a part, at the end of the export a warning is issued

Thus for every part either set a `SKU` with the OPL part number or an `MPN`
value.

Add the plugin in eeschema, set it a name, then use it with `Generate`:

![BOM plugin screenshot](img/bom_plugin.png)

## License

Copyright 2017 Gergely Imreh <imrehg@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
