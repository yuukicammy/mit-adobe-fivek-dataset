#include <iostream>
#include <libraw.h>
#include <sstream>
#include <stdexcept>
#include <string>

int main(int argc, char *argv[]) {

  try {
    LibRaw raw;
    std::string input_filename =
        "/Users/ytra/Desktop/a0541-050618_215910__MG_2944.dng";

    // Open a ProRaw file.
    {
      int res = raw.open_file(input_filename.c_str());
      if (res != LIBRAW_SUCCESS) {
        throw std::runtime_error("LibRaw failed to read file: " +
                                 input_filename);
      }
    }

    // Initial processing
    {
      int res = raw.unpack();
      if (res != LIBRAW_SUCCESS) {
        throw std::runtime_error("LibRaw failed to unpack. file: " +
                                 input_filename);
      }
    }

    std::cout << "make:\t" << raw.imgdata.idata.make << std::endl;
    std::cout << "model:\t" << raw.imgdata.idata.model << std::endl;
    std::cout << "normalized_make:\t" << raw.imgdata.idata.normalized_make
              << std::endl;
    std::cout << "normalized_model:\t" << raw.imgdata.idata.normalized_model
              << std::endl;
    return 0;

  } catch (std::exception &e) {
    std::cerr << e.what() << std::endl;
    return 1;
  }
}