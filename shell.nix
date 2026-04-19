{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {

  buildInputs = [
    pkgs.stdenv.cc.cc.lib
  ];
  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
}

