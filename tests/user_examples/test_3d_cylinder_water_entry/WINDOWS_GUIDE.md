# Windows系统完整配置指南

## 📌 系统要求

- Windows 10/11（64位）
- 至少8GB内存
- 至少20GB可用磁盘空间
- 处理器：建议4核以上

## 🛠️ 软件安装步骤

### 1. 安装Visual Studio（C++编译器）⭐必需

#### 方法A：Visual Studio Community（推荐，功能完整）

1. **下载**
   - 访问：https://visualstudio.microsoft.com/zh-hans/downloads/
   - 下载 "Visual Studio 2022 Community"（免费）

2. **安装**
   - 运行安装程序
   - 在"工作负荷"选项卡中，勾选：
     - ✅ **"使用C++的桌面开发"**
   - 在右侧"安装详细信息"中，确保包含：
     - ✅ MSVC v143 - VS 2022 C++ x64/x86生成工具
     - ✅ Windows 10/11 SDK
     - ✅ CMake工具（在"单个组件"选项卡中搜索添加）
   - 点击"安装"（大约需要10-20GB空间）

3. **验证安装**
   - 打开 "开始菜单" → 搜索 "Developer Command Prompt for VS 2022"
   - 在命令提示符中输入：
     ```cmd
     cl
     ```
   - 如果看到版本信息，说明安装成功

#### 方法B：Visual Studio Build Tools（轻量级，仅编译功能）

如果不需要完整的IDE：

1. 下载：https://visualstudio.microsoft.com/zh-hans/downloads/#build-tools-for-visual-studio-2022
2. 安装时选择 "使用C++的桌面开发"
3. 安装大小约5GB

### 2. 安装CMake ⭐必需

1. **下载**
   - 访问：https://cmake.org/download/
   - 选择 "Windows x64 Installer"（例如：cmake-3.28.x-windows-x86_64.msi）

2. **安装**
   - 运行安装程序
   - **重要**：勾选 "Add CMake to the system PATH for all users"
   - 点击"Install"

3. **验证安装**
   - 打开新的命令提示符（CMD）
   - 输入：
     ```cmd
     cmake --version
     ```
   - 应该显示CMake版本号

### 3. 安装ParaView（可选，用于3D可视化）⭐推荐

1. **下载**
   - 访问：https://www.paraview.org/download/
   - 下载Windows 64位版本

2. **安装**
   - 运行安装程序
   - 默认选项即可

### 4. 配置Python环境（您已有）✅

您已经有Anaconda和conda环境，只需添加必要的包：

```cmd
conda activate SPH
conda install numpy matplotlib
```

## 📥 下载和配置SPHinXsys

### 使用Git Bash（您已安装）

1. **打开Git Bash**

2. **创建工作目录并克隆仓库**
   ```bash
   # 在D盘创建目录
   cd /d
   mkdir SPHinXsys
   cd SPHinXsys

   # 克隆仓库
   git clone https://github.com/zhtoiv/SPHinXsys.git
   cd SPHinXsys

   # 切换到包含圆柱体入水项目的分支
   git checkout claude/sph-cylinder-simulation-fwCT7
   ```

## 🔨 编译项目

### 方法1：使用批处理脚本（最简单）⭐推荐

1. **打开 Developer Command Prompt for VS 2022**
   - 在开始菜单搜索并打开

2. **运行脚本**
   ```cmd
   cd D:\SPHinXsys\SPHinXsys\tests\user_examples\test_3d_cylinder_water_entry
   run_simulation_windows.bat
   ```

这个脚本会自动完成：
- ✅ 配置CMake
- ✅ 编译项目
- ✅ 运行仿真
- ✅ 数据分析（如果检测到Python）

### 方法2：手动编译（更灵活）

#### 2.1 打开Developer Command Prompt

**重要**：必须在Visual Studio的开发者命令提示符中操作！

在开始菜单搜索：
- "Developer Command Prompt for VS 2022"
- 或 "x64 Native Tools Command Prompt for VS 2022"

#### 2.2 配置CMake

```cmd
cd D:\SPHinXsys\SPHinXsys
mkdir build
cd build

REM 配置项目（首次需要）
cmake .. -G "Visual Studio 17 2022" -A x64
```

可能的CMake生成器选项：
- Visual Studio 17 2022 (推荐)
- Visual Studio 16 2019
- Visual Studio 15 2017
- Ninja (需要额外安装)

#### 2.3 编译

**编译整个SPHinXsys库**（首次需要，需要较长时间）：
```cmd
cmake --build . --config Release -j 8
```

**仅编译圆柱体入水项目**：
```cmd
cmake --build . --config Release --target test_3d_cylinder_water_entry -j 8
```

参数说明：
- `--config Release`：发布版本（速度快）
- `--config Debug`：调试版本（可调试，但慢）
- `-j 8`：使用8个CPU核心并行编译（根据您的CPU调整）

#### 2.4 查找可执行文件

编译完成后，可执行文件位于：
```
D:\SPHinXsys\SPHinXsys\build\tests\user_examples\test_3d_cylinder_water_entry\Release\bin\test_3d_cylinder_water_entry.exe
```

## 🚀 运行仿真

### 方法1：命令行运行

```cmd
cd D:\SPHinXsys\SPHinXsys\build\tests\user_examples\test_3d_cylinder_water_entry\Release\bin

test_3d_cylinder_water_entry.exe
```

### 方法2：双击运行

直接双击 `test_3d_cylinder_water_entry.exe`

### 运行时输出

仿真运行时会显示：
```
========================================
3D Cylinder Water Entry Simulation
========================================
Cylinder - Diameter: 40 mm
         - Height: 300 mm
         - Mass: 0.4 kg
         - Density: 10638.298 kg/m^3
         - Entry velocity: 10 m/s
Water    - Length: 1 m
         - Width: 0.2 m
         - Height: 0.8 m
         - Density: 1000 kg/m^3
Particle spacing: 2 mm
========================================
Simulation started...
N=100  Time=0.010000  Dt=0.001000  dt=0.000100
N=200  Time=0.020000  Dt=0.001000  dt=0.000100
...
```

## 📊 数据分析

### 使用Anaconda环境分析

1. **打开Anaconda Prompt**

2. **激活环境并运行分析**
   ```cmd
   conda activate SPH

   cd D:\SPHinXsys\SPHinXsys\tests\user_examples\test_3d_cylinder_water_entry

   python analyze_motion.py ^
     D:\SPHinXsys\SPHinXsys\build\tests\user_examples\test_3d_cylinder_water_entry\Release\bin\output ^
     D:\SPHinXsys\SPHinXsys\build\tests\user_examples\test_3d_cylinder_water_entry\Release\bin\analysis_results
   ```

   注意：Windows命令行中使用 `^` 作为续行符

3. **查看结果**
   ```cmd
   explorer D:\SPHinXsys\SPHinXsys\build\tests\user_examples\test_3d_cylinder_water_entry\Release\bin\analysis_results
   ```

### 生成的图表

- `displacement.png` - 位移曲线
- `velocity.png` - 速度曲线
- `acceleration.png` - 加速度曲线
- `forces.png` - 力分析
- `energy.png` - 能量演化
- `simulation_summary.txt` - 统计摘要

## 🎨 3D可视化（ParaView）

### 打开ParaView

1. 启动ParaView
2. File → Open
3. 浏览到输出目录：
   ```
   D:\SPHinXsys\SPHinXsys\build\tests\user_examples\test_3d_cylinder_water_entry\Release\bin\output
   ```
4. 选择所有 `.vtp` 文件（或选择特定的body文件）
5. 点击 "Apply"

### ParaView操作技巧

**着色变量**：
- 选择 "Pressure" 查看压力分布
- 选择 "Velocity" 查看速度场
- 选择 "Density" 查看密度分布

**播放动画**：
- 点击工具栏的播放按钮 ▶
- 查看圆柱体入水过程

**创建切面**：
1. 选择body
2. Filters → Common → Clip
3. 调整切面位置和方向

**显示速度矢量**：
1. Filters → Common → Glyph
2. 选择 Glyph Type: Arrow
3. Vectors: Velocity

## ⚠️ 常见问题解决

### 问题1：找不到 `cl.exe` 或编译器

**原因**：没有在Visual Studio开发者命令提示符中运行

**解决**：
- 必须使用 "Developer Command Prompt for VS 2022"
- 不要使用普通的CMD或PowerShell

### 问题2：CMake找不到编译器

**原因**：Visual Studio安装不完整

**解决**：
1. 打开 Visual Studio Installer
2. 点击 "修改"
3. 确保勾选了 "使用C++的桌面开发"
4. 在右侧确保包含 MSVC 编译器

### 问题3：编译时内存不足

**原因**：并行编译占用内存过多

**解决**：
```cmd
REM 减少并行任务数
cmake --build . --config Release -j 2
```

### 问题4：找不到可执行文件

**原因**：路径错误或编译失败

**解决**：
1. 检查编译输出是否有错误
2. 手动查找exe文件：
   ```cmd
   dir /s test_3d_cylinder_water_entry.exe
   ```

### 问题5：Python分析脚本报错

**可能原因1**：缺少Python包

**解决**：
```cmd
conda activate SPH
pip install numpy matplotlib
```

**可能原因2**：找不到数据文件

**解决**：
- 确保仿真已成功运行
- 检查output目录是否存在
- 使用绝对路径运行分析脚本

### 问题6：仿真运行很慢

**优化建议**：
1. 使用Release模式编译（不是Debug）
2. 减少粒子分辨率：
   ```cpp
   // 在 cylinder_water_entry.cpp 中修改
   Real particle_spacing_ref = cylinder_diameter / 10.0;  // 从20改为10
   ```
3. 减少仿真时间：
   ```cpp
   Real end_time = 0.5;  // 从1.0改为0.5秒
   ```
4. 设置并行线程：
   ```cmd
   set OMP_NUM_THREADS=8
   test_3d_cylinder_water_entry.exe
   ```

## 📁 文件结构说明

```
D:\SPHinXsys\SPHinXsys\
├── tests\user_examples\test_3d_cylinder_water_entry\
│   ├── cylinder_water_entry.cpp       # 源代码
│   ├── CMakeLists.txt                 # 编译配置
│   ├── analyze_motion.py              # 分析脚本
│   ├── run_simulation_windows.bat     # Windows运行脚本
│   ├── run_simulation.sh              # Linux运行脚本
│   ├── README.md                      # 详细文档
│   ├── QUICKSTART.md                  # 快速开始
│   └── WINDOWS_GUIDE.md               # 本文件
│
└── build\
    └── tests\user_examples\test_3d_cylinder_water_entry\Release\bin\
        ├── test_3d_cylinder_water_entry.exe   # 可执行文件
        ├── output\                             # 仿真输出
        │   ├── *.vtp                          # ParaView文件
        │   └── *.dat                          # 数据文件
        └── analysis_results\                   # 分析结果
            ├── *.png                          # 图表
            └── simulation_summary.txt         # 摘要
```

## 🎓 学习资源

- **SPHinXsys官网**：https://www.sphinxsys.org/
- **GitHub仓库**：https://github.com/Xiangyu-Hu/SPHinXsys
- **ParaView教程**：https://www.paraview.org/tutorials/
- **SPH方法介绍**：查看项目README.md

## 💡 性能优化建议

### 硬件优化
- **CPU**：使用多核处理器，设置 `OMP_NUM_THREADS`
- **内存**：建议16GB以上
- **硬盘**：使用SSD可加快编译和I/O

### 软件优化
1. **使用Release模式**：
   ```cmd
   cmake --build . --config Release
   ```

2. **调整粒子分辨率**：
   - 粗糙快速：`cylinder_diameter / 10`
   - 标准：`cylinder_diameter / 20`
   - 精细慢速：`cylinder_diameter / 40`

3. **减少输出频率**：
   ```cpp
   Real output_interval = 0.02;  // 增加输出间隔
   ```

4. **并行编译**：
   ```cmd
   cmake --build . -j %NUMBER_OF_PROCESSORS%
   ```

## 📞 获取帮助

遇到问题时：
1. 查看本指南的"常见问题"部分
2. 查看项目README.md
3. 检查SPHinXsys GitHub Issues
4. 访问SPHinXsys官方论坛

---

**祝您使用愉快！** 🎉

如有任何问题，欢迎提出。
