{
  inputs = { nixpkgs.url = "github:nixos/nixpkgs"; };

  outputs = { self, nixpkgs }:
    let pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in {
      devShell.x86_64-linux =
        pkgs.mkShell { 
          name = "python-devel";
          venvDir = "venv";
          buildInputs = with pkgs.python311Packages; [
            pandas
            scipy
            numpy
            jupyter
            venvShellHook
            pyarrow
          ] ++ (with pkgs; [ ta-lib ]); 
        };
   };
}
