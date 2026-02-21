/**
 * VS Code Git Extension API Type Definitions
 * Based on vscode.git extension API
 */

import { Uri, Event, Disposable, ProviderResult } from 'vscode';

export interface API {
  readonly repositories: Repository[];
  readonly state: APIState;
  readonly onDidOpenRepository: Event<Repository>;
  readonly onDidCloseRepository: Event<Repository>;
  readonly onDidChangeState: Event<APIState>;
  toGitUri(uri: Uri, ref: string): Uri;
  getRepository(uri: Uri): Repository | null;
}

export type APIState = 'uninitialized' | 'initialized';

export interface Repository {
  readonly rootUri: Uri;
  readonly inputBox: InputBox;
  readonly state: RepositoryState;
  readonly ui: RepositoryUIState;
  
  getConfigs(): Promise<{ key: string; value: string }[]>;
  getConfig(key: string): Promise<string>;
  setConfig(key: string, value: string): Promise<string>;
  getGlobalConfig(key: string): Promise<string>;
  
  getObjectDetails(treeish: string, path: string): Promise<{ mode: string; object: string; size: number }>;
  detectObjectType(object: string): Promise<{ mimetype: string; encoding?: string }>;
  buffer(ref: string, path: string): Promise<Buffer>;
  show(ref: string, path: string): Promise<string>;
  getCommit(ref: string): Promise<Commit>;
  
  add(resources: Uri[]): Promise<void>;
  revert(resources: Uri[]): Promise<void>;
  clean(resources: Uri[]): Promise<void>;
  
  apply(patch: string, reverse?: boolean): Promise<void>;
  diff(cached?: boolean): Promise<string>;
  diffWithHEAD(path: string): Promise<string>;
  diffWith(ref: string, path: string): Promise<string>;
  diffIndexWithHEAD(path: string): Promise<string>;
  diffIndexWith(ref: string, path: string): Promise<string>;
  diffBlobs(object1: string, object2: string): Promise<string>;
  diffBetween(ref1: string, ref2: string, path: string): Promise<string>;
  
  hashObject(data: string): Promise<string>;
  
  commit(message: string, opts?: CommitOptions): Promise<void>;
  
  checkout(treeish: string): Promise<void>;
  
  findTrackingBranches(upstreamRef: string): Promise<Branch[]>;
  
  getBranch(name: string): Promise<Branch>;
  getBranches(query: BranchQuery): Promise<Ref[]>;
  setBranchUpstream(name: string, upstream: string): Promise<void>;
  
  getMergeBase(ref1: string, ref2: string): Promise<string>;
  
  status(): Promise<void>;
  
  tag(name: string, upstream: string): Promise<void>;
  deleteTag(name: string): Promise<void>;
  
  fetch(remote?: string, ref?: string, depth?: number): Promise<void>;
  pull(unshallow?: boolean): Promise<void>;
  push(remoteName?: string, branchName?: string, setUpstream?: boolean): Promise<void>;
  
  blame(path: string): Promise<string>;
  log(options?: LogOptions): Promise<Commit[]>;
}

export interface InputBox {
  value: string;
}

export interface RepositoryState {
  readonly HEAD: Branch | undefined;
  readonly refs: Ref[];
  readonly remotes: Remote[];
  readonly submodules: Submodule[];
  readonly rebaseCommit: Commit | undefined;
  
  readonly mergeChanges: Change[];
  readonly indexChanges: Change[];
  readonly workingTreeChanges: Change[];
  
  readonly onDidChange: Event<void>;
}

export interface RepositoryUIState {
  readonly selected: boolean;
  readonly onDidChange: Event<void>;
}

export interface Branch extends Ref {
  readonly type: RefType.Head | RefType.RemoteHead;
  readonly name?: string;
  readonly upstream?: UpstreamRef;
  readonly ahead?: number;
  readonly behind?: number;
}

export interface UpstreamRef {
  readonly remote: string;
  readonly name: string;
}

export interface Ref {
  readonly type: RefType;
  readonly name?: string;
  readonly commit?: string;
  readonly remote?: string;
}

export enum RefType {
  Head,
  RemoteHead,
  Tag
}

export interface Remote {
  readonly name: string;
  readonly fetchUrl?: string;
  readonly pushUrl?: string;
  readonly isReadOnly: boolean;
}

export interface Submodule {
  readonly name: string;
  readonly path: string;
  readonly url: string;
}

export interface Change {
  readonly uri: Uri;
  readonly originalUri: Uri;
  readonly renameUri: Uri | undefined;
  readonly status: Status;
}

export enum Status {
  INDEX_MODIFIED,
  INDEX_ADDED,
  INDEX_DELETED,
  INDEX_RENAMED,
  INDEX_COPIED,
  
  MODIFIED,
  DELETED,
  UNTRACKED,
  IGNORED,
  INTENT_TO_ADD,
  
  ADDED_BY_US,
  ADDED_BY_THEM,
  DELETED_BY_US,
  DELETED_BY_THEM,
  BOTH_ADDED,
  BOTH_DELETED,
  BOTH_MODIFIED
}

export interface Commit {
  readonly hash: string;
  readonly message: string;
  readonly parents: string[];
  readonly authorDate?: Date;
  readonly authorName?: string;
  readonly authorEmail?: string;
  readonly commitDate?: Date;
}

export interface CommitOptions {
  all?: boolean | 'tracked';
  amend?: boolean;
  signoff?: boolean;
  signCommit?: boolean;
  empty?: boolean;
  noVerify?: boolean;
  requireUserConfig?: boolean;
}

export interface BranchQuery {
  readonly remote?: boolean;
  readonly pattern?: string;
  readonly count?: number;
  readonly contains?: string;
}

export interface LogOptions {
  readonly maxEntries?: number;
  readonly path?: string;
  readonly range?: string;
  readonly reverse?: boolean;
  readonly sortByAuthorDate?: boolean;
}

export interface GitExtension {
  readonly enabled: boolean;
  readonly onDidChangeEnablement: Event<boolean>;
  getAPI(version: 1): API;
}

export default GitExtension;
