$targetDir = "e:\git\DormitoryCultureFestival\frontend\public\特质匹配图片"

if (-not (Test-Path $targetDir)) {
    Write-Host "错误：找不到目录 $targetDir" -ForegroundColor Red
    Write-Host "请确保您已将'特质匹配图片'文件夹复制到 frontend/public/ 目录下。" -ForegroundColor Yellow
    exit
}

$files = Get-ChildItem $targetDir -File
$count = 0

foreach ($file in $files) {
    # 使用正则表达式替换零宽空格和其他不可见字符
    # \u200B 是零宽空格
    $cleanName = $file.Name -replace "[\u200B\u200C\u200D\uFEFF]", ""
    
    if ($file.Name -ne $cleanName) {
        $newPath = Join-Path $targetDir $cleanName
        Rename-Item -Path $file.FullName -NewName $cleanName
        Write-Host "重命名: '$($file.Name)' -> '$cleanName'" -ForegroundColor Green
        $count++
    }
}

if ($count -eq 0) {
    Write-Host "检查完毕，未发现需要修复的文件名。" -ForegroundColor Cyan
} else {
    Write-Host "成功修复了 $count 个文件名。" -ForegroundColor Cyan
}
