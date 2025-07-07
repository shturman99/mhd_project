nprocx:=2
nprocy:=2


nprocz= $(ncpus)/($(nprocx)*$(nprocy))
nprocx := $(shell echo $$(($(nprocx))))
nprocy := $(shell echo $$(($(nprocy))))
nprocz := $(shell echo $$(($(nprocz))))
