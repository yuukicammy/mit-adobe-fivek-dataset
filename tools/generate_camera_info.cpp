/**
 * The MIT License
 * Copyright (c) {2023} yuukicammy
 *
 * @file
 * @brief Generate camera information from DNG files under the specified
 * directory.
 *
 * This program lists camera information of DNG files under the specified
 * directory. The camera information is output in a CSV file.
 *
 * Usage:
 *    Genrate Camera Information [OPTION...]
 *
 *    -r, --root_dir arg  Path of the root directory where DNG files are
 *                        searched. (default:
 *                        /datasets/MITAdobeFiveK/raw/fivek_dataset/raw_photos)
 *    -o, --outfile arg   Path of the output CSV file. (default:
 *                        ./data/camera_models.csv)
 *    -h, --help          Print usage.
 *
 */

#include "cxxopts.hpp"
#include <filesystem>
#include <fstream>
#include <iostream>
#include <libraw.h>
#include <stdexcept>
#include <string>

/**
 * @brief Function to determine if the extension is ".dng" or not.
 *
 * @param[in] path file path
 * @return true if file path is ".dng".
 * @return false if file path is not ".dng".
 */
bool is_dng_file(const std::string &path) {
  return path.substr(path.size() - 4) == ".dng";
}

/**
 * Get the base name of a file from its path.
 *
 * @param path File path.
 * @return Base name of the file.
 */
std::string basename(const std::string &path) {
  auto pos = path.find_last_of("/\\");
  auto filename = path.substr(pos + 1);
  return filename.substr(0, filename.size() - 4);
}

/**
 * Get the camera maker and model information from a DNG file.
 *
 * @param raw LibRaw instance for processing the DNG file.
 * @param filename File path of the DNG file.
 * @return Comma-separated camera make and model information. Each element means
 * file_id, make, normalized_make, model, and normalized_model.
 */
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

/**
 * Main entry point of the program.
 *
 * @param argc Number of command-line arguments.
 * @param argv Array of command-line arguments.
 * @return Exit code of the program (0 for success, non-zero for error).
 */
int main(int argc, char *argv[]) {
  cxxopts::Options options(
      "Genrate Camera Information",
      "This program lists camera information of DNG files under the specified "
      "directory. The camera information is output in a CSV file.\n");
  options.add_options()(
      "r,root_dir", "Path of the root directory where DNG files are searched.",
      cxxopts::value<std::string>()->default_value(
          "/datasets/MITAdobeFiveK/raw/fivek_dataset/raw_photos"));
  options.add_options()(
      "o,outfile", "Path of the output CSV file.",
      cxxopts::value<std::string>()->default_value("./data/camera_models.csv"));
  options.add_options()("h,help", "Print usage.");

  auto args = options.parse(argc, argv);
  if (args.count("help")) {
    std::cout << options.help() << std::endl;
    options.show_positional_help();
    return 0;
  }

  try {
    LibRaw raw;
    const std::string in_dir = args["root_dir"].as<std::string>();
    const std::string out_file = args["outfile"].as<std::string>();

    if (in_dir.empty() || out_file.empty()) {
      throw std::invalid_argument(options.help());
    }

    std::ofstream file;
    file.open(out_file, std::ios::out);
    file << "file_id,make,normalized_make,model,normalized_model\n";

    std::filesystem::path root_dir{in_dir};

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
    options.show_positional_help();
    std::cout << options.help() << std::endl;
    std::cerr << e.what() << std::endl;
    return 1;
  }
}