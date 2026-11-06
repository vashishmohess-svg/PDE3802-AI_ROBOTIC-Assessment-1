# Step 3.5.5K.4 - Approved Group-Aware Dataset Split

**Decision date:** 6 November 2026
**Decision maker:** Member 1 - Project Lead
**Decision:** APPROVED - Adopt the proposed group-aware split for model development and final evaluation.

## 1. Decision

The project lead has approved the proposed group-aware dataset split
based on the candidate relationship review and conservative grouping
analysis completed in Step 3.5.5K.

The approved split assignments are defined by the existing full split
manifest. The manifest is the authoritative source of proposed
train, validation and test assignments.

## 2. Approved split counts

| Split | Original images | Approved proposed images |
|---|---:|---:|
| Training | 816 | 813 |
| Validation | 223 | 226 |
| Testing | 103 | 103 |
| **Total** | **1,142** | **1,142** |

Proposed proportions:

- Training: approximately 71.19%
- Validation: approximately 19.79%
- Testing: approximately 9.02%

The effective training set contains 812 eligible images because one
previously identified severely pixelated Pencil image remains excluded
from effective training:

`Pencil/00038_jpg.rf.7f94c208054cb0f13467f3967c7ed71c.jpg`

This image remains in the original dataset and is not deleted.

## 3. Evidence supporting the decision

The review and grouping evidence records:

- 48 candidate pairs independently adjudicated by Member 2.
- 31 classified as SHARED_SOURCE_PHOTO_SUPPORTED.
- 16 classified as UNRESOLVED.
- 1 classified as RELATED_BUT_DISTINCT_PHOTOGRAPHS (Candidate 007).
- 44 candidate images represented in 13 conservative connected groups.
- All 47 supported and unresolved relationships verified within
  their respective proposed groups and proposed splits.
- Candidate 007 remains separate from the conservative groups.
- All eight classes remain represented in all three proposed splits.
- The manifest contains 1,142 records, with no duplicate class/filename
  records, invalid split values or missing original source images.

The conservative grouping treats unresolved relationships as
potentially related for split allocation. It does not reclassify them
as confirmed duplicates.

The connected groups are candidate relationship groups. Their
membership does not prove that every image in a group derives from
an identical source photograph.

## 4. Dataset preservation

The original `dataset/` directory must remain unchanged.

This approval does not move, copy, rename, delete or overwrite original
images. It approves the use of the manifest to determine the split
assignments used by subsequent project code.

The original on-disk split counts remain:

- Train: 816
- Valid: 223
- Test: 103

The proposed assignments must be applied through a manifest-driven
loader or another reproducible derived-data approach. The original
dataset folders must not be manually rearranged.

## 5. Model development and test-set protection

During Step 3, model fitting must use only the approved training
assignments. Baseline evaluation must use the approved validation
assignments.

During Step 4, model comparison and selection must use training and
validation data only.

The approved test assignments must remain unused for model fitting,
model selection, hyperparameter tuning and iterative development.
The proposed test set is reserved for the final held-out evaluation
in Step 6.

## 6. Limitations and interpretation

The split allocation was manually configured and checked for
relationship containment and class balance. It has not been proven
to be a globally optimal allocation.

The analysis addresses the candidate relationships identified in
the completed review. It does not prove that every possible duplicate
or source-image relationship in the full dataset has been identified.

The 16 unresolved relationships remain unresolved. The decision to
group them conservatively is a precaution for split allocation, not
a claim that they are confirmed duplicates.

## 7. Authoritative manifest and evidence hashes

Approved proposed split manifest:

`docs/evidence/step3.5.5J/step3.5.5K3_full_split_manifest_proposal.csv`

Original Member 1 Windows working-copy SHA256 (CRLF line endings):

`B5389FB8368A18AD54649B87A3EB6ABB47BC29FF0D0B373A6B86054B7CCA477D`

Member 2 adjudication file:

`docs/evidence/step3.5.5J/member2_adjudication.csv`

Original Member 1 Windows working-copy SHA256 (CRLF line endings):

`28038526fe0c93ff2bc5ba723b65f8d090795a5ecf6bc6c4644a821997dae4de`

Conservative group membership file:

`docs/evidence/step3.5.5J/step3.5.5K3_conservative_group_membership.csv`

Original Member 1 Windows working-copy SHA256 (CRLF line endings):

`5548BEA4ED1C7C5CBA2E5F1E88E9246E578BD2172FADB73F7181CBE4EFD14CB5`

## 8. Git line-ending normalisation and canonical committed hashes

The original hashes in Section 7 identify Member 1's Windows working-copy
files, which use CRLF line endings.

A subsequent byte-level diagnostic compared those files with the exact
committed Git objects at commit:

`14ade034758ad304318e8a7dafeaf4c6ff84d968`

The diagnostic established that Git stored the CSV files using LF
line endings. Member 1's Git system configuration has
`core.autocrlf=true`, and no `.gitattributes` rule overrides the
line-ending behaviour for these files.

For each of the three files, replacing CRLF with LF in the original
working-copy bytes produced a byte-for-byte match with the committed
Git object. Therefore, the hash differences are caused exclusively
by line-ending normalisation, not by differences in CSV content.

Canonical committed Git-file SHA256 values (LF line endings):

| Evidence file | Canonical committed SHA256 |
|---|---|
| `step3.5.5K3_full_split_manifest_proposal.csv` | `40FAD2A63BF4BA3185731154D1F5908901F5D224FD3F2D098FAE84C9B234B7D5` |
| `member2_adjudication.csv` | `AE2F9D1BD5F02A58700DD900430A3181B4DC3BCB288397BF547698A842735BE4` |
| `step3.5.5K3_conservative_group_membership.csv` | `FEDB0089E8A62255E78F87A288E48A0EFDBF9D7CD72AB4C42006C874B25B995D` |

The original Windows working-copy hashes remain preserved in Section 7.
Both hash forms identify the same logical file content under different
line-ending representations.

The diagnostic did not modify the CSV files or the dataset.

Detailed diagnostic evidence is recorded in:

`docs/evidence/step3.5.5J/step3.5.5K4_git_hash_normalization_verification.txt`

## 9. Approval status

The project lead's approval is recorded on 6 November 2026.

This document records the decision to use the proposed manifest for
subsequent model development and final evaluation. Member 2 must
independently verify the manifest hash and split counts before the
team treats the approved manifest as shared project evidence.

No classifier training or final test evaluation is authorised by
this decision-recording step itself.
