# Báo Cáo Bài Tập 4: Quản Lý Tệp Tin Bỏ Qua (.gitignore) Và Sửa Đổi Lịch Sử Commit (Amend)

- **Môn học**: DevOps Fundamentals (IT-209)
- **Session**: 04 - Git Version Control
- **Bài tập**: Bài 4 - Quản lý tệp tin bỏ qua (.gitignore) và Sửa lịch sử (Amend)
- **Đường dẫn nộp bài trên GitHub**: `homework/session_04/ex4/`
- **Học viên**: HoQuocKhai
- **Email**: khaiho6040@gmail.com

---

## 1. Mục tiêu bài thực hành
1. **Cấu hình tệp `.gitignore` chuẩn mực**: Nắm vững cú pháp thiết lập tệp cấu hình `.gitignore` để tự động loại bỏ các tệp tin chứa thông tin nhạy cảm (secrets, credentials, API keys) và các tệp rác hệ thống (build cache, virtual environments) khỏi sự theo dõi của Git.
2. **Gỡ bỏ an toàn tệp đã theo dõi khỏi Git Cache (`git rm --cached`)**: Hiểu sâu cơ chế tách biệt giữa thư mục làm việc vật lý (**Working Directory**) và bộ nhớ đệm lập chỉ mục (**Staging Area / Index**). Gỡ bỏ tệp tin khỏi sự quản lý của Git mà tuyệt đối không làm mất dữ liệu vật lý trên ổ cứng.
3. **Sửa đổi lịch sử commit gần nhất với `--amend`**: Sử dụng lệnh `git commit --amend` để viết đè và thay thế commit sai sót trước đó, loại bỏ tệp nhạy cảm và cập nhật thông điệp commit chuẩn mực, bảo đảm lịch sử kho chứa sạch sẽ.
4. **Kiểm tra và xác thực toàn diện**: Kiểm tra trạng thái kho chứa (`git status`), commit gần nhất (`git log -n 1`), quy tắc bỏ qua (`git check-ignore`), và tính toàn vẹn của tệp vật lý trên đĩa cứng.

---

## 2. Bối cảnh và Rủi ro bảo mật trong thực tế

### 2.1. Nguy cơ khi vô tình commit Credentials / Secrets lên Git
Trong quá trình phát triển phần mềm, lập trình viên thường tạo các tệp cấu hình cục bộ chứa mật khẩu cơ sở dữ liệu, API tokens, Private keys (`credentials.txt`, `.env`). 
- Nếu sử dụng lệnh `git add .` thiếu cẩn trọng, các tệp này sẽ bị đóng gói vào commit.
- Khi mã nguồn được đẩy lên các dịch vụ đám mây công khai (GitHub, GitLab), các bot tự động quét mã nguồn (Secrets Scanners) có thể thu thập các thông tin xác thực này trong vòng vài giây, dẫn đến nguy cơ lộ lọt dữ liệu nghiêm trọng, chiếm đoạt tài nguyên đám mây hoặc bị tấn công tống tiền.

### 2.2. Tại sao xóa vật lý tệp tin bằng lệnh OS (`rm` / `del`) là sai lầm?
- Khi xóa file vật lý (`del credentials.txt` hoặc `rm credentials.txt`), lập trình viên sẽ **mất hoàn toàn cấu hình cần thiết để chạy ứng dụng trên máy cục bộ**.
- Quan trọng hơn, việc xóa file bằng OS sau đó commit mới (`git commit -m "delete credentials"`) **không hề xóa tệp khỏi lịch sử Git**. Tệp nhạy cảm vẫn tồn tại vĩnh viễn trong commit cũ trước đó và bất kỳ ai cũng có thể `git checkout` về commit cũ để lấy cắp thông tin!
- **Giải pháp đúng đắn**: Dùng `git rm --cached` để chỉ gỡ tệp khỏi Git index, thêm vào `.gitignore` và dùng `git commit --amend` để loại bỏ hoàn toàn dấu vết tệp khỏi commit.

---

## 3. Quá trình thực hiện chi tiết

### Bước 1: Khởi tạo Local Repository và cấu hình danh tính cục bộ
```bash
git init -b main
git config --local user.name "HoQuocKhai"
git config --local user.email "khaiho6040@gmail.com"
```

### Bước 2: Tạo tệp ứng dụng `main.py` và tệp cấu hình bí mật `credentials.txt`
Tạo tệp mã nguồn `main.py`:
```python
import os

def load_system_config():
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    return {"host": db_host, "port": db_port, "environment": "production"}

if __name__ == "__main__":
    print(load_system_config())
```

Tạo tệp chứa thông tin nhạy cảm `credentials.txt` phục vụ môi trường nội bộ:
```text
# ==============================================================================
# CONFIDENTIAL DATABASE & API CREDENTIALS - DO NOT COMMIT TO VERSION CONTROL
# ==============================================================================
DB_HOST=database.internal.prod.net
DB_PORT=5432
DB_NAME=devops_production
DB_USER=super_admin
DB_PASSWORD=P@ssw0rd_Super_Secret_2026!
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
API_SECRET_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.devops.secret
```

---

### Bước 3: Mô phỏng hành vi vô tình commit tệp nhạy cảm
Giả định tình huống học viên vô tình đưa toàn bộ tệp vào Staging và thực hiện commit đầu tiên:
```bash
git add .
git commit -m "feat: initial commit with main.py and credentials.txt"
```
**Kết quả thực tế:**
```text
[main (root-commit) 2804f4f] feat: initial commit with main.py and credentials.txt
 2 files changed, 37 insertions(+)
 create mode 100644 credentials.txt
 create mode 100644 main.py
```
Kiểm tra danh sách tệp đang bị theo dõi bằng `git ls-files`:
```bash
git ls-files
```
**Kết quả:**
```text
credentials.txt
main.py
```
*Đánh giá*: Tệp `credentials.txt` đã bị theo dõi và lưu trữ trong commit `2804f4f`. Cần xử lý khẩn cấp trước khi đẩy lên remote.

---

### Bước 4: Gỡ bỏ tệp nhạy cảm khỏi bộ đệm theo dõi của Git (`git rm --cached`)
Thực thi lệnh gỡ bỏ `credentials.txt` khỏi Git Index mà không xóa file vật lý:
```bash
git rm --cached credentials.txt
```
**Kết quả thực tế:**
```text
rm 'credentials.txt'
```

Kiểm tra trạng thái bằng `git status`:
```bash
git status
```
**Kết quả thực tế:**
```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	deleted:    credentials.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	credentials.txt
```
*Phân tích*:
- Trong mục `Changes to be committed`, Git ghi nhận thao tác `deleted: credentials.txt` (sẵn sàng gỡ tệp khỏi commit tiếp theo).
- Trong mục `Untracked files`, tệp `credentials.txt` vẫn tồn tại trên đĩa cứng cục bộ nhưng chưa được theo dõi.

---

### Bước 5: Cấu hình tệp `.gitignore` để bỏ qua tệp nhạy cảm
Tạo tệp `.gitignore` trong thư mục gốc dự án:
```gitignore
# Sensitive credentials & secrets (Security Protection)
credentials.txt
*.env
*.pem
*.key
secrets/

# Python cache & build files
__pycache__/
*.py[cod]
*.pyo
.venv/
env/

# OS & Editor temporary files
.vscode/
.idea/
.DS_Store
Thumbs.db
```

Kiểm tra lại `git status` sau khi tạo `.gitignore`:
```bash
git status
```
**Kết quả thực tế:**
```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	deleted:    credentials.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
```
*Quan sát*: `credentials.txt` đã **hoàn toàn biến mất** khỏi danh sách `Untracked files` vì đã được quy tắc trong `.gitignore` bảo vệ!

Đưa `.gitignore` vào Staging Area:
```bash
git add .gitignore
```

---

### Bước 6: Sửa đổi commit gần nhất bằng `git commit --amend`
Sử dụng cờ `--amend` để gộp các thay đổi trong Staging (xóa `credentials.txt` khỏi index, thêm `.gitignore`) vào chính commit trước đó và cập nhật thông điệp mới:
```bash
git commit --amend -m "feat: initial project setup without sensitive files"
```
**Kết quả thực tế:**
```text
[main c643e39] feat: initial project setup without sensitive files
 Date: Mon Oct 5 21:29:57 2026 +0700
 2 files changed, 45 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 main.py
```
*Phân tích*: Commit mới mang hash `c643e39` đã thay thế hoàn toàn commit cũ `2804f4f`. Trong commit mới này, chỉ có 2 tệp được lưu giữ là `.gitignore` và `main.py`. Tệp `credentials.txt` đã được loại bỏ hoàn toàn khỏi lịch sử Git.

---

### Bước 7: Xác minh tệp vật lý `credentials.txt` vẫn nguyên vẹn trên đĩa cứng
Kiểm tra sự tồn tại của tệp trên hệ thống tệp cục bộ (PowerShell):
```powershell
Test-Path credentials.txt
```
**Kết quả:**
```text
True
```
Lệnh `dir credentials.txt` hoặc `Get-Item credentials.txt` hiển thị tệp tin vẫn đầy đủ kích thước và nội dung 100% nguyên vẹn.

---

## 4. Cơ chế hoạt động của `git rm --cached` và `git commit --amend`

```mermaid
flowchart LR
    subgraph WD["1. Working Directory (Ổ đĩa cục bộ)"]
        F1["main.py"]
        F2["credentials.txt (Giữ nguyên vẹn)"]
        F3[".gitignore"]
    end

    subgraph SA["2. Staging Area (Git Index / Cache)"]
        S1["main.py"]
        S2["credentials.txt -> BỊ XÓA KHỎI INDEX"]
        S3[".gitignore (Được thêm mới)"]
    end

    subgraph Repo["3. Local Repository (Git History)"]
        C1["Commit cũ (2804f4f)<br/>Chứa credentials.txt (Bị hủy bỏ)"]
        C2["Commit Amend (c643e39)<br/>Chỉ gồm main.py + .gitignore"]
    end

    F2 -.->|"git rm --cached"| S2
    F3 -->|"git add .gitignore"| S3
    SA -->|"git commit --amend"| C2
    C1 -.->|"Bị thay thế hoàn toàn"| C2

    classDef wd fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef sa fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef repo fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    class WD wd;
    class SA sa;
    class Repo repo;
```

### So sánh các lệnh xóa trong Git:
| Lệnh | Working Directory (Ổ cứng) | Staging Area (Index) | Ứng dụng |
| :--- | :--- | :--- | :--- |
| `rm file` (Lệnh OS) | **Đã xóa** | Vẫn còn theo dõi | Thao tác sai lầm |
| `git rm file` | **Đã xóa** | Đánh dấu xóa (`deleted`) | Muốn xóa vĩnh viễn cả code và file |
| `git rm --cached file` | **Vẫn giữ nguyên vẹn** | Đánh dấu xóa khỏi theo dõi | **Gỡ file nhạy cảm khỏi Git an toàn** |

---

## 5. Kết quả kiểm tra theo yêu cầu đề bài

### 5.1. Kiểm tra trạng thái Git (`git status`)
```bash
git status
```
**Kết quả thực tế:**
```text
On branch main
nothing to commit, working tree clean
```
*Nhận xét*: 
- Tệp `credentials.txt` không còn xuất hiện ở bất kỳ trạng thái nào (không Staged, không Modified, không Untracked).
- Trạng thái thư mục làm việc hoàn toàn sạch sẽ (`working tree clean`).

---

### 5.2. Kiểm tra commit gần nhất (`git log -n 1`)
```bash
git log -n 1
```
**Kết quả thực tế:**
```text
commit c643e399bfad0db98935c2ad708010d16f2f91cc (HEAD -> main)
Author: HoQuocKhai <khaiho6040@gmail.com>
Date:   Mon Oct 5 21:29:57 2026 +0700

    feat: initial project setup without sensitive files
```
*Nhận xét*: Thông điệp commit đã được cập nhật thành công qua `--amend`, phản ánh đúng trạng thái mã nguồn sạch sẽ.

---

### 5.3. Kiểm tra quy tắc tệp bỏ qua (`git check-ignore`)
```bash
git check-ignore -v credentials.txt
```
**Kết quả thực tế:**
```text
.gitignore:2:credentials.txt    credentials.txt
```
*Nhận xét*: Git xác nhận tệp `credentials.txt` đang được tự động bỏ qua bởi quy tắc tại dòng số 2 của `.gitignore`.

---

### 5.4. Kiểm tra danh sách tệp được Git quản lý (`git ls-files`)
```bash
git ls-files
```
**Kết quả thực tế:**
```text
.gitignore
main.py
```
*Nhận xét*: Chỉ có `.gitignore` và `main.py` nằm trong danh sách theo dõi, `credentials.txt` đã biến mất hoàn toàn khỏi Git Index.

---

## 6. Ảnh chụp màn hình minh chứng

### Minh chứng 1: Sơ đồ luồng cơ chế `git rm --cached` và `git commit --amend`
![Minh chứng cơ chế gỡ cache và sửa lịch sử commit](1.png)

### Minh chứng 2: Chạy toàn bộ các lệnh thao tác và kiểm tra trên Terminal
![Minh chứng kết quả chạy lệnh git rm --cached, git status, git commit --amend trên Terminal](2.png)

---

## 7. Khuyến nghị và Quy tắc an toàn bảo mật (DevOps Best Practices)
1. **Thiết lập `.gitignore` ngay khi khởi tạo dự án**: Luôn tạo tệp `.gitignore` đầu tiên trước khi thêm bất kỳ tệp mã nguồn nào.
2. **Sử dụng tệp mẫu môi trường (`.env.example`)**: Chỉ commit các tệp định dạng khung như `.env.example` chứa danh sách các biến không có giá trị nhạy cảm thật để làm tài liệu hướng dẫn cho đồng nghiệp.
3. **Quản lý Secrets bằng Secret Manager chuyên dụng**: Sử dụng các giải pháp an toàn như HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, hoặc GitHub Actions Secrets thay vì lưu trữ dạng plain-text trên ổ cứng.
4. **Cài đặt Pre-commit Hooks (Git-secrets, TruffleHog)**: Thiết lập các công cụ tự động quét mã nguồn trước mỗi commit để chặn đứng hành vi commit nhầm credentials ngay tại local máy trạm.
