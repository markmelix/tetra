{
  description = "Minimalistic code editor";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      pythonEnv = pkgs.python3.withPackages (ps: with ps; [
        pyqt5
        qscintilla
        charset-normalizer
      ]);
    in {
      packages.${system}.default = pkgs.stdenv.mkDerivation {
        pname = "tetra";
        version = "1.0.0";
        src = ./.;

        nativeBuildInputs = [
          pkgs.libsForQt5.wrapQtAppsHook
          pkgs.makeWrapper
        ];

        buildInputs = [
          pythonEnv
          pkgs.qt5.qtbase
          pkgs.qt5.qtsvg
          pkgs.qt5.qttools
        ];

        installPhase = ''
          mkdir -p $out/bin
          cat > $out/bin/tetra <<EOF
          #!${pkgs.bash}/bin/bash
          exec ${pythonEnv}/bin/python $out/src/main.py "\$@"
          EOF
          chmod +x $out/bin/tetra

          mkdir -p $out/src
          cp -r src/* $out/src/
          cp -r resources $out/
        '';

        postFixup = ''
          wrapQtApp $out/bin/tetra
        '';
      };

      apps.${system}.default = {
        type = "app";
        program = "${self.packages.${system}.default}/bin/tetra";
      };

      devShells.${system}.default = pkgs.mkShell {
        nativeBuildInputs = [
          pkgs.libsForQt5.wrapQtAppsHook
          pkgs.makeWrapper
        ];

        buildInputs = [
          pythonEnv
          pkgs.qt5.qtbase
          pkgs.qt5.qtsvg
          pkgs.qt5.qttools
        ];

        shellHook = ''
          echo "Tetra development environment ready."
          echo "Run: python src/main.py"
        '';
      };
    };
}
