function iccasm=iccasmoptions(varargin)
%ICCASMOPTIONS - CG + ASM with sub-block ICC preconditioner
%
%   Symmetric counterpart of iluasmoptions. Use this for symmetric
%   positive-definite operators (e.g. SSA stressbalance, thermal
%   diffusion). CG is the optimal Krylov method for SPD; ICC is the
%   SPD analogue of ILU and gives the same fill-in/conditioning
%   trade-off without breaking symmetry.
%
%   PETSc's ICC is sequential, so we wrap it in ASM for parallel runs.
%
%   Usage:
%      options=iccasmoptions;

%retrieve options provided in varargin
options=pairoptions(varargin{:});
iccasm=struct();
iccasm.toolkit='petsc';
iccasm.mat_type=getfieldvalue(options,'mat_type','aij');
iccasm.ksp_type=getfieldvalue(options,'ksp_type','cg');
iccasm.pc_type=getfieldvalue(options,'pc_type','asm');
iccasm.sub_pc_type=getfieldvalue(options,'sub_pc_type','icc');
iccasm.pc_asm_overlap=getfieldvalue(options,'pc_asm_overlap',5);
iccasm.ksp_max_it=getfieldvalue(options,'ksp_max_it',100);
iccasm.ksp_rtol=getfieldvalue(options,'ksp_rtol',1e-8);
