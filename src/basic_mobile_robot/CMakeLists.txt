cmake_minimum_required(VERSION 3.8)
project(basic_mobile_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# Starts the installation instruction
install( 
  # Tells CMake to install the entire urdf folder
  DIRECTORY 
  urdf 
  launch
  worlds
  
  DESTINATION share/${PROJECT_NAME} 
)

install( # Starts the installation instruction for the Python teleoperation program
  PROGRAMS scripts/custom_teleop.py # Installs custom_teleop.py as an executable program
  DESTINATION lib/${PROJECT_NAME} # Places the executable in the package's lib directory
)

ament_package()
