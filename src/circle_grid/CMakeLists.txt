if(OpenCV_FOUND)
camodocal_library(camodocal_circle_grid SHARED
  CircleGrid.cc
)

camodocal_link_libraries(camodocal_circle_grid
  ${CAMODOCAL_PLATFORM_UNIX_LIBRARIES}
  ${OpenCV_LIBS}
)

camodocal_install(camodocal_circle_grid)
endif(OpenCV_FOUND)
