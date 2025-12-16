@echo off
REM ============================================================================
REM Windows批处理脚本 - 3D圆柱体入水仿真
REM ============================================================================

echo ========================================================================
echo 3D Cylinder Water Entry Simulation - Windows Build and Run
echo ========================================================================

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
set PROJECT_NAME=test_3d_cylinder_water_entry

REM 设置构建配置（可改为Debug用于调试）
set BUILD_CONFIG=Release

REM 检查是否在Visual Studio命令提示符中
where cl.exe >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 未检测到Visual Studio编译器！
    echo 请在 "Visual Studio Developer Command Prompt" 中运行此脚本
    echo.
    echo 或者按以下步骤操作:
    echo 1. 打开开始菜单
    echo 2. 搜索 "Developer Command Prompt for VS"
    echo 3. 在该命令提示符中运行此脚本
    echo.
    pause
    exit /b 1
)

echo.
echo 步骤 1: 配置CMake项目...
echo ------------------------------------------------------------------------

cd /d "%SCRIPT_DIR%..\..\.."

if not exist "build" mkdir build
cd build

REM 配置CMake（仅首次需要，后续可跳过）
if not exist "CMakeCache.txt" (
    echo 首次配置，正在生成Visual Studio项目文件...
    cmake .. -G "Visual Studio 17 2022" -A x64
    if %ERRORLEVEL% NEQ 0 (
        echo [错误] CMake配置失败！
        pause
        exit /b 1
    )
    echo [完成] CMake配置成功
) else (
    echo [跳过] CMake已配置
)

echo.
echo 步骤 2: 编译项目...
echo ------------------------------------------------------------------------

echo 正在编译 %PROJECT_NAME% (%BUILD_CONFIG% 模式)...
cmake --build . --config %BUILD_CONFIG% --target %PROJECT_NAME% -j 8

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 编译失败！
    echo.
    echo 常见问题：
    echo - 确保已安装Visual Studio及C++组件
    echo - 检查是否有足够的磁盘空间
    echo - 尝试清理后重新编译: cmake --build . --config %BUILD_CONFIG% --target clean
    echo.
    pause
    exit /b 1
)

echo [完成] 编译成功！

echo.
echo 步骤 3: 运行仿真...
echo ------------------------------------------------------------------------

set EXE_PATH=tests\user_examples\%PROJECT_NAME%\%BUILD_CONFIG%\bin
if exist "%EXE_PATH%\%PROJECT_NAME%.exe" (
    cd "%EXE_PATH%"
    echo 开始仿真计算...
    echo 可执行文件: %CD%\%PROJECT_NAME%.exe
    echo.

    %PROJECT_NAME%.exe

    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [完成] 仿真运行成功！
    ) else (
        echo.
        echo [错误] 仿真运行失败！
        pause
        exit /b 1
    )
) else (
    echo [错误] 找不到可执行文件: %EXE_PATH%\%PROJECT_NAME%.exe
    echo.
    echo 当前目录: %CD%
    echo 预期路径: %EXE_PATH%\%PROJECT_NAME%.exe
    pause
    exit /b 1
)

echo.
echo 步骤 4: 数据分析...
echo ------------------------------------------------------------------------

REM 检查Python
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo 检测到Python，开始分析数据...

    if not exist "analysis_results" mkdir analysis_results

    python "%SCRIPT_DIR%analyze_motion.py" "%CD%\output" "%CD%\analysis_results"

    if %ERRORLEVEL% EQU 0 (
        echo [完成] 数据分析成功！
        echo 结果保存在: %CD%\analysis_results\
    ) else (
        echo [警告] 数据分析失败
        echo.
        echo 您可以手动运行分析:
        echo conda activate SPH
        echo python "%SCRIPT_DIR%analyze_motion.py" "%CD%\output" "%CD%\analysis_results"
    )
) else (
    echo [跳过] 未检测到Python
    echo.
    echo 请在Anaconda Prompt中运行数据分析:
    echo conda activate SPH
    echo cd "%SCRIPT_DIR%"
    echo python analyze_motion.py "%CD%\output" "%CD%\analysis_results"
)

echo.
echo ========================================================================
echo 仿真流程完成！
echo ========================================================================
echo.
echo 输出位置:
echo   - 可执行文件: %EXE_PATH%\%PROJECT_NAME%.exe
echo   - VTP文件 (ParaView): %CD%\output\
echo   - 数据文件 (DAT): %CD%\output\
if exist "%CD%\analysis_results" (
    echo   - 分析结果: %CD%\analysis_results\
)
echo.
echo 下一步操作:
echo   1. 使用ParaView打开VTP文件查看3D可视化
echo      ParaView下载: https://www.paraview.org/download/
echo.
echo   2. 查看分析结果图表（如果已生成）
echo      explorer "%CD%\analysis_results"
echo.
echo   3. 查看原始数据文件
echo      explorer "%CD%\output"
echo.
echo ========================================================================

pause
