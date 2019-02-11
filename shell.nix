{ nixpkgs ? import <nixpkgs> {} }:

let
   pythonPackages = nixpkgs.python37Packages;
   python = pythonPackages.python;
   pythonLibraries = with pythonPackages; [
     sphinx flit
   ];

in nixpkgs.stdenv.mkDerivation rec {
  name = "pylogtree-dev-env";
  env = nixpkgs.buildEnv { name = name; paths = buildInputs; };
  buildInputs = pythonLibraries ++ [python];
}
