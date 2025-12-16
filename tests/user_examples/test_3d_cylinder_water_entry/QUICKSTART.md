# Quick Start Guide - 3D Cylinder Water Entry Simulation

## 快速开始指南

这是一个使用SPH方法进行圆柱体入水仿真的完整项目。

### 项目特点

✅ **仿真计算** - 记录6自由度运动数据
✅ **粒子可视化** - 生成3D粒子图像（ParaView）
✅ **运动数据分析** - 自动生成位移、速度、加速度曲线

### 仿真参数

| 参数 | 值 |
|------|-----|
| 圆柱体直径 | 40 mm |
| 圆柱体高度 | 300 mm |
| 圆柱体质量 | 0.4 kg |
| 入水速度 | 10 m/s (向下) |
| 水域尺寸 | 1.0m × 0.2m × 0.8m |

## 一键运行（推荐）

```bash
cd tests/user_examples/test_3d_cylinder_water_entry
./run_simulation.sh
```

这个脚本会自动完成：
1. ✓ 编译项目
2. ✓ 运行仿真
3. ✓ 分析数据并生成图表

## 手动操作

### 步骤 1: 编译

```bash
cd tests/user_examples/test_3d_cylinder_water_entry
mkdir build && cd build
cmake ..
make -j$(nproc)
```

### 步骤 2: 运行仿真

```bash
cd bin
./test_3d_cylinder_water_entry
```

仿真运行时会显示进度：
```
========================================
3D Cylinder Water Entry Simulation
========================================
Cylinder - Diameter: 40 mm
         - Height: 300 mm
         - Mass: 0.4 kg
         ...
Simulation started...
N=100  Time=0.010000  Dt=0.001000  dt=0.000100
...
```

### 步骤 3: 分析结果

```bash
# 在 build/bin 目录下
python3 ../../analyze_motion.py ./output ./analysis_results
```

## 输出文件说明

### 📊 可视化文件（VTP格式，用ParaView打开）

位置：`build/bin/output/`

- `WaterBody_*.vtp` - 水粒子状态
- `Cylinder_*.vtp` - 圆柱体粒子状态
- `WallBoundary_*.vtp` - 边界墙

**ParaView使用提示：**
```bash
paraview build/bin/output/*.vtp
```

在ParaView中：
- 选择变量着色：Pressure（压力）、Velocity（速度）
- 播放动画查看入水过程
- 使用Clip过滤器创建剖面图

### 📈 运动数据文件（DAT格式）

位置：`build/bin/output/`

**6自由度运动数据：**
- `CylinderObserver_Position.dat` - 位置
- `CylinderObserver_Velocity.dat` - 速度
- `CylinderObserver_AccelerationPrior.dat` - 加速度

**力数据：**
- `Cylinder_ViscousForceFromFluid.dat` - 粘性力
- `Cylinder_PressureForceFromFluid.dat` - 压力

**能量数据：**
- `Cylinder_TotalMechanicalEnergy.dat` - 机械能

### 📉 分析结果（自动生成）

位置：`build/bin/analysis_results/`

- `displacement.png` - 位移曲线（x, y, z方向及总位移）
- `velocity.png` - 速度曲线（x, y, z方向及速度大小）
- `acceleration.png` - 加速度曲线（x, y, z方向及加速度大小）
- `forces.png` - 力分析（粘性力、压力、总力、阻力系数）
- `energy.png` - 能量演化曲线
- `simulation_summary.txt` - 数值统计摘要

## 常见问题

### Q: 编译失败怎么办？

**A:** 确保已经正确编译安装SPHinXsys：
```bash
# 回到SPHinXsys根目录
cd /path/to/SPHinXsys
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### Q: 仿真速度太慢？

**A:** 可以调整以下参数（在 `cylinder_water_entry.cpp` 中）：
```cpp
Real particle_spacing_ref = cylinder_diameter / 10.0;  // 降低分辨率（从20改为10）
Real end_time = 0.5;  // 缩短仿真时间（从1.0改为0.5）
```

### Q: 如何修改仿真参数？

**A:** 编辑 `cylinder_water_entry.cpp` 中的参数：
```cpp
// 修改圆柱体尺寸
Real cylinder_diameter = 0.04;      // 直径 [m]
Real cylinder_height = 0.3;         // 高度 [m]

// 修改入水速度
Vecd cylinder_initial_velocity(0.0, 0.0, -10.0);  // [m/s]

// 修改水域大小
Real water_length = 1.0;            // [m]
Real water_width = 0.2;             // [m]
Real water_height = 0.8;            // [m]
```

修改后需要重新编译：
```bash
cd build
make -j$(nproc)
```

### Q: Python分析脚本报错？

**A:** 安装所需依赖：
```bash
pip3 install numpy matplotlib
```

如果使用seaborn样式报错，编辑 `analyze_motion.py`：
```python
# 将
plt.style.use('seaborn-v0_8-darkgrid')
# 改为
plt.style.use('default')
```

## 性能优化建议

1. **并行计算** - 设置OpenMP线程数：
   ```bash
   export OMP_NUM_THREADS=8
   ./test_3d_cylinder_water_entry
   ```

2. **降低输出频率** - 减少文件I/O：
   ```cpp
   Real output_interval = 0.02;  // 从0.01改为0.02
   ```

3. **粒子排序** - 已自动启用（每100步）

## 典型结果

运行完成后，您将看到：

- **最大穿透深度** - 圆柱体进入水中的最大深度
- **速度变化** - 从初速度10m/s到最终速度的变化过程
- **入水冲击力** - 最大压力峰值和粘性力
- **能量耗散** - 机械能随时间的变化

## 项目结构

```
test_3d_cylinder_water_entry/
├── cylinder_water_entry.cpp    # 主程序（仿真代码）
├── CMakeLists.txt              # 编译配置
├── analyze_motion.py           # 数据分析脚本
├── run_simulation.sh           # 一键运行脚本
├── README.md                   # 详细文档
└── QUICKSTART.md              # 本文件
```

## 进一步学习

- 完整文档：查看 `README.md`
- SPHinXsys官网：https://www.sphinxsys.org/
- SPHinXsys示例：查看 `tests/3d_examples/` 目录

## 获取帮助

如有问题：
1. 查看 `README.md` 的故障排除部分
2. 访问 SPHinXsys GitHub Issues
3. 检查 SPHinXsys 官方文档

---

**祝您仿真顺利！** 🚀
