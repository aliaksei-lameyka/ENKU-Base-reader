# R144 visual routing review / Проверка подозрительных мест

Read-only review materials. **Review is OPEN; no copper has been changed. NO FAB.**

## Как отмечать

Откройте `ENKU_R144_F_Cu_Review_Map.png` в исходном разрешении3750×5950. Обведите подозрительные места синими кругами и пронумеруйте1,2,3… Не закрашивайте саму дорожку. Сохраняйте ориентацию платы и координатные линейки; для мелкого участка приложите также увеличенный фрагмент. Пояснение полезно, но необязательно: достаточно показать место. Координаты — фактические X/Y платы в мм, Y направлен вниз. Bottom показан без зеркалирования.

Для каждого номера фиксируем: координаты, слой, цепь и ближайшие компоненты; что проверено в исходнике, схеме, других слоях и Gerber; вывод и основание. Статусы: `ACCEPTABLE WITH REASON`, `EDIT REQUIRED`, `CALCULATION/MEASUREMENT PENDING`. Снимок одного слоя сам по себе не доказывает замыкание или обрыв.

Параллельно проходим всю плату по функциональным узлам. Проверяем дубликаты и наложения, петли и ненужные ответвления, сужения, переходные отверстия, зазоры, пути прямого и обратного токов, питание/развязку, переключающие узлы и обратную связь, USB, e-paper, SPI/microSD, загрузку/сброс и антенную область. Наличие параллельного пути питания или земли не означает ошибку: удаление требует проверки его функции.

После согласованного исправления сравниваем исходник и медь до/после, заново выполняем DRC/ERC, проверку связности исходника и независимую связность Gerber, обновляем экспорты и пакет. Физические измерения остаются отдельным этапом.

## English review procedure

Use numbered blue circles on the full-resolution Top Copper PNG. Keep copper visible, preserve orientation and rulers, and include a close-up for small features. The four-layer ZIP also contains vector SVG maps for unlimited zoom. Board coordinates are in mm, Y increases downwards; Bottom is unmirrored. These are engineering review images, not manufacturing-scale artwork.

For each annotation, identify location, net, layers and components; inspect the editable source, schematic and actual manufacturing Gerbers; assess connectivity, width/neckdowns, via roles, source/return paths and manufacturer layout guidance. Record a reasoned disposition using the statuses above. Inspect the whole board by functional block in addition to user annotations. Same-net power/GND meshes and width transitions need individual assessment; do not automatically delete them for appearance.

After any hardware edit, rerun native and independent checks, compare before/after copper and regenerate the source-pinned exports. Visual review and static checks do not replace startup, load-step, ripple, thermal, ESD or EMC measurements.

## Executed read-only preparation

- Revision R144, PCB SHA256 `676c157fb58c1d5b689b4a6841749d8be283982745ce40580c0a33308f7e2d2c`.
- Input: actual source-pinned GitHub run38693384483, source commit `609f8ac00357b9b0c6b3c43c381469c498453a11`; downloaded artifact SHA256 `c29fc94e2c5712441b1858481e0da9d4f703f8b14362db15b49594aa49b8ca17`.
- All native SVG drawing groups are preserved in the maps. Rulers add X=18..77mm/Y=20..121mm; anchor R72.1 is X65.15/Y70.00mm. No source or manufacturing bytes changed.
-3606 routed non-via tracks inspected geometrically on four copper layers. Found21 same-net closed centerline faces outside pads,15 partial collinear overlaps and23 exact coincident segment pairs. These are59 candidate records, **not59 proven defects or59 necessarily distinct locations**. All dispositions remain OPEN.
- Candidate thresholds: closed-face area outside same-net pads buffered0.02mm >=0.005mm²; collinear overlap outside pads >=0.05mm. Exact duplicate requires equal geometry and width. Synthetic closed/open/partial-overlap detector cases passed.
- The original suspicious 3V3_SYS area near C11/R16/R99, approximately X56..60/Y94..97mm, appears in the closed-face candidate list. This local recognition is not a functional clearance of the rest of the board.
- The detector does not assess filled-plane meshes, impedance, current capacity, 3D contact geometry, hidden schematic errors or dynamic behavior. It supplements existing native/Gerber verification.

Reproduce with Python3, PyMuPDF and Shapely2.2:

```sh
python docs/r144_visual_review.py PATH_TO_EXTRACTED_NATIVE_CI_CANDIDATE OUTPUT_DIRECTORY
```

The JSON includes input hashes and segment UUIDs; CSV is a compact review queue. No automatic cleanup is performed. Prior physical qualification holds remain open.

Primary references: [KiCad10 PCB Editor](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html), [TI TPS63802 datasheet, layout section](https://www.ti.com/lit/ds/symlink/tps63802.pdf). For U4 specifically, check short/direct input/output capacitor paths, power/control ground routing and feedback separation from switching nodes against the TI requirements.
