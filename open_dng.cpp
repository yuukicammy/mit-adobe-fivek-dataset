#include <filesystem>
#include <fstream>
#include <iostream>
#include <libraw.h>
#include <stdexcept>
#include <string>

bool is_dng_file(const std::string &path) {
  return path.substr(path.size() - 4) == ".dng";
}

std::string basename(const std::string &path) {
  auto pos = path.find_last_of("/\\");
  auto filename = path.substr(pos + 1);
  return filename.substr(0, filename.size() - 4);
}

std::string camera_model(LibRaw &raw, const std::string &filename) {
  raw.recycle();
  {
    int res = raw.open_file(filename.c_str());
    if (res != LIBRAW_SUCCESS) {
      return "";
    }
  }
  // Initial processing
  {
    int res = raw.unpack();
    if (res != LIBRAW_SUCCESS) {
      return "";
    }
  }
  return std::string{raw.imgdata.idata.make} + "," +
         std::string{raw.imgdata.idata.normalized_make} + "," +
         std::string{raw.imgdata.idata.model} + "," +
         std::string{raw.imgdata.idata.normalized_model};
}

int main(int argc, char *argv[]) {
  try {
    LibRaw raw;
    std::string out_file = "../camera_models.txt";

    std::ofstream file;
    file.open(out_file, std::ios::out);
    file << "file_id,make,normalized_make,model,normalized_model\n";

    std::filesystem::path root_dir{
        "../../MITAboveFiveK/raw/fivek_dataset/raw_photos/"};

    for (const auto &entry :
         std::filesystem::recursive_directory_iterator(root_dir)) {
      if (!entry.is_directory() && is_dng_file(entry.path())) {
        std::string &&camera_info = camera_model(raw, entry.path());
        file << basename(entry.path()) << "," << camera_info << "\n";
      }
    }
    file.close();
    return 0;

  } catch (std::exception &e) {
    std::cerr << e.what() << std::endl;
    return 1;
  }
}