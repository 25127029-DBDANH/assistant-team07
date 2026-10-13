# Data sources and owners

This file documents every data file in this repository: where the data comes
from, who is responsible for it, and how often it should be updated.

## Summary

| File | Source | Owner | Update frequency |
|------|--------|-------|------------------|
| `data/offices.csv` | public_material (https://github.com/CSC10014-at-fit-hcmus) | Lam Le & LamNotNam1607 | mỗi buổi lab |

## Details

### `data/offices.csv`

- **Content:** file chứa: danh sách văn phòng, số phòng, giờ mở cửa, ngày hoạt động trong tuần
- **Columns:** các cột có trong file: name, room, hour
- **Source:** nguồn dữ liệu: public material, link: https://github.com/CSC10014-at-fit-hcmus
- **Owner:** Lam Le (@LamNotNam1607)
- **Update frequency:** khi nào cần kiểm tra lại
- **Last verified:** 5/10/2026

## How to update a data file

1. Create a branch and edit the file.
2. Run `pytest -q`.
3. Open a pull request that links the issue, and ask the owner to review.