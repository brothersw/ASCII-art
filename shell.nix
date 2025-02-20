# shell.nix
let
  pkgs = import <nixpkgs> {};

  python = pkgs.python3;

in pkgs.mkShell {
  packages = [
    (python.withPackages (python-pkgs: [
      # select Python packages here
      python-pkgs.numpy
      python-pkgs.pillow
    ]))
  ];
}
