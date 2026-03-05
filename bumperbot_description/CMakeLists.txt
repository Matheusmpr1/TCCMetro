cmake_minimum_required(VERSION 3.8)
project(bumperbot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# --- NOVIDADE AQUI ---
# Instala o script Python como um executável do sistema
install(PROGRAMS
  scripts/lidar_alarm.py
  DESTINATION lib/${PROJECT_NAME}
)

# Mantém a instalação das suas pastas originais
install(
  DIRECTORY meshes urdf launch rviz
  DESTINATION share/${PROJECT_NAME}
)
# ---------------------

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()