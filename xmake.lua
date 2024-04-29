add_requires("pybind11")

rule("inline_py")
    set_extensions(".h", ".cc", ".cpp")
    add_deps("c++")

    on_load(function (target)
        target:add("defines", "compile_time_inline")

        -- add .xx
        local rule = target:rule("c++.build"):clone()
        rule:set("extensions", ".h", ".cc", ".cpp")
        target:rule_add(rule)

        -- patch sourcebatch for .xx
        local sourcebatch = target:sourcebatches()["c++.build"]
        sourcebatch.sourcekind = "cxx"
        sourcebatch.objectfiles = {}
        sourcebatch.dependfiles = {}

        for _, sourcefile in ipairs(sourcebatch.sourcefiles) do
            local objectfile = target:objectfile(sourcefile)
            local dependfile = target:dependfile(objectfile)
            table.insert(sourcebatch.objectfiles, objectfile)
            table.insert(sourcebatch.dependfiles, dependfile)
        end

        -- force as c++ source file
        if target:is_plat("windows") then
            target:add("cxxflags", "/TP")
        else
            target:add("cxxflags", "-x c++")
        end
    end)

    before_build(function (target)
        print("before_build")
        local rootdir = path.join(target:autogendir(), "rules", "inline_py")
        local filename = "inline_py_gen.h"
        local sourcefile_cx = target:autogenfile(filename, {rootdir = rootdir, filename = filename})
        local sourcefile_dir = path.directory(sourcefile_cx)

        os.tryrm(sourcefile_cx)
        os.mkdir(sourcefile_dir)
        target:add("includedirs", sourcefile_dir, {public = public})
        print("tryrm %s", sourcefile_cx)
    end)

    before_build_files(function (target, sourcebatch, opt)
        print("before_build_files", sourcebatch.sourcefiles)
        local rootdir = path.join(target:autogendir(), "rules", "inline_py")
        local filename = "inline_py_gen.h"
        local sourcefile_cx = target:autogenfile(filename, {rootdir = rootdir, filename = filename})
        local sourcefile_dir = path.directory(sourcefile_cx)

        local argv = {"pp.py", "-o", sourcefile_cx}
        for _, sourcefile in ipairs(sourcebatch.sourcefiles) do
            print("before_build_files: %%%d: %s", opt.progress, sourcefile)
            -- 对这些文件调用 pp.py
            table.insert(argv, "-i")
            table.insert(argv, sourcefile)
        end
        print("try run %s", argv)
        os.vrunv("python3", argv)
    end)


target("sample")
    set_kind("binary")
    set_languages("c++17")
    add_rules("inline_py")
    add_packages("pybind11")
    add_rpathdirs("/Library/Developer/CommandLineTools/Library/Frameworks/")
    add_files("sample.cc")

