{
  description = "PGI Python development environment";

  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: rec {
	postgres = pkgs.mkShell {
              nativeBuildInputs = with pkgs; [
		      glibcLocales
		      lsof
		      pgcli
		      postgresql_16
		      procps
	      ];
        };

        venv = pkgs.mkShell {
          venvDir = ".venv";
          packages = with pkgs; [ python312 ] ++
            (with pkgs.python312Packages; [
	      android-tools
	      flet
	      flutter
              pip
              venvShellHook
            ]) ++ (with pkgs; [
              pandoc
	      texlive.combined.scheme-full
	    ]);
	  nativeBuildInputs = postgres.nativeBuildInputs;
        };

	default = venv;

        server = pkgs.mkShell {
          venvDir = ".venv";
          packages = with pkgs; [ python312 ] ++
            (with pkgs.python312Packages; [
              pip
              venvShellHook
            ]);
	  nativeBuildInputs = with pkgs; [
              pgcli
              postgresql_16
	  ];
        };
      });
    };
}
